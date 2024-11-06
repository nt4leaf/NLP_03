import streamlit as st
from sub1 import model_pred

video_id = st.text_input('Enter YouTube URL')
st.markdown(
    """
    <meta http-equiv="refresh" content="5">
    """,
    unsafe_allow_html=True
)
if video_id:
    model_pred(video_id)


