# Input widgets for the main area
import streamlit as st
import json
import time
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

@st.cache_data
def call_cortex_llm(prompt_text):
    """Makes a call to Cortex AI with the given prompt."""
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    response_raw = df.collect()[0][0]
    return json.loads(response_raw)

st.subheader(":material_input: Input content")
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")

# Configuration widgets moved to the sidebar
with st.sidebar:
    st.title(":material_post: LinkedIn Post Generator v3")
    st.success("An app for generating LinkedIn post using content from input link.")
    tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
    word_count = st.slider("Approximate word count:", 50, 300, 100)

if st.button("Generate Post"):
    with st.status("Starting engine...", expanded=True) as status:

        # Step 1: Construct Prompt
        st.write(":material_psychology: Thinking: Analyzing constraints and tone...")
        time.sleep(2)

        prompt = f"""
            You are an expert social media manager. Generate a LinkedIn post based on the following:

            Tone: {tone}
            Desired Length: Approximately {word_count} words
            Use content from this URL: {content}

            Generate only the LinkedIn post text. Use dash for bullet points.
            """

        # Step 2: Call API
        st.write(":material_flash_on: Generating: contacting Snowflake Cortex...")
        time.sleep(2)

        response = call_cortex_llm(prompt)

        # Step 3: Update Status to Complete
        st.write(":material_check_circle: Post generation completed!")
        status.update(label="Post Generated Successfully!", state="complete", expanded=False)

    st.subheader("Generated Post:")
    st.markdown(response)