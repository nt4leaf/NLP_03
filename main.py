import streamlit as st
from sub1 import model_pred


placeholder = st.empty()
video_id = st.text_input('Enter Video ID')

# Kiểm tra nếu có dữ liệu nhập vào
if video_id:
    placeholder.success('Processing')
    result = model_pred(video_id)
    placeholder.empty()
    if not result:
        placeholder.error('Invalid Video ID!')
else:
    placeholder.empty()


