import re
import streamlit as st
from sub1 import model_pred

def extract_video_id(url):
    # Sử dụng regex để tìm ID video
    video_id = re.search(r'(?<=v=)[^&#]+', url)
    if not video_id:
        video_id = re.search(r'(?<=be/)[^&#]+', url)
    return video_id.group(0) if video_id else None

link = st.text_input('Enter YouTube URL')
if link:
    video_id = extract_video_id(link)
    if not video_id:
        st.error('Invalid YouTube URL')
    else:
        st.success(f'Video ID: {video_id}')
        model_pred(video_id)
    st.text("Success_ALL")

