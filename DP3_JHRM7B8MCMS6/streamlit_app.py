# https://discuss.streamlit.io/t/the-30-days-of-ai-challenge-starts-today/120455
# https://30daysofai.streamlit.app

import streamlit as st

# Auto-detect environment and connect
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Query and display Snowflake version
version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]

st.success(f"Successfully connected! Snowflake Version: {version}")