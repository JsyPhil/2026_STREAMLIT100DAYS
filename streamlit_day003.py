import streamlit as st
from snowflake.cortex import Complete
import time

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Model selection
llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
model = st.selectbox("Select a model", llm_models)

# Prompt input 
example_prompt = "What is Python?"
prompt = st.text_area("Enter prompt", example_prompt)

# Choose streaming method (direct or custom generator)
streaming_method = st.radio(
    "Streaming Method:",
    ["Direct (stream=True)", "Custom Generator"],
    help="Choose how to stream the response"
)

# Generate response
if st.button("Generate Response"):
    with st.spinner(f"Generating response with `{model}`"):
        if streaming_method == "Direct (stream=True)":
            stream_generator = Complete(
                session=session,
                model=model,
                prompt=prompt,
                stream=True,  # Built-in streaming
            )
            st.write_stream(stream_generator)
        else:
            # Custom streaming method
            def custom_stream_generator():
                """
                Alternative streaming method for cases where
                the generator is not compatible with st.write_stream
                """
                output = Complete(
                    session=session,
                    model=model,
                    prompt=prompt  # No stream parameter
                )
                for chunk in output:
                    yield chunk
                    time.sleep(0.01)  # Small delay for smooth streaming
            
            st.write_stream(custom_stream_generator)



# Footer
st.divider()
st.caption("Day 3: Hello, Cortex! | 30 Days of AI")