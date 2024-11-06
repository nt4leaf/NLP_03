import streamlit as st
from sub1 import model_pred

video_id = st.text_input('Enter YouTube URL')
if video_id:
    model_pred(video_id)


