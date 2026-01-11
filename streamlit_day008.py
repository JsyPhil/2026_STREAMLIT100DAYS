import streamlit as st

with st.chat_message("user"):
    st.write("Hello! Can you explain what Streamlit is?")

with st.chat_message("assistant"):
    st.write("Streamlit is an open-source Python framework for building data apps.")
    st.bar_chart([10, 20, 30, 40]) 

prompt = st.chat_input("Type a message here...")

if prompt:
    # Display the user's new message
    with st.chat_message("user"):
        st.write(prompt)

    # Display a mock assistant response
    with st.chat_message("assistant"):
        st.write(f"You just said:\n\n '{prompt}' \n\n(I don't have memory yet!)")