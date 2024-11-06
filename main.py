import streamlit as st
from sub1 import model_pred

video_id = st.text_input('Enter Video ID')

if video_id:
    result = model_pred(video_id)
    if not result:
        st.text('Invalid Video ID')

