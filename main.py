import re
import streamlit as st
from sub1 import video_comments
from sub2 import text_processing
def extract_video_id(url):
    # Sử dụng regex để tìm ID video
    video_id = re.search(r'(?<=v=)[^&#]+', url)
    if not video_id:
        video_id = re.search(r'(?<=be/)[^&#]+', url)
    return video_id.group(0) if video_id else None

def cmt_processing(video_id):
    comment = video_comments(video_id)
    clear_text = text_processing(comment)
    # clear_text_padded = comments_youtube.padding(tokenize(clear_text))
    return clear_text

# Giao diện Streamlit
st.title('YouTube Video ID Extractor')

# Nhập liên kết YouTube
link = st.text_input('Enter YouTube URL')

# Hiển thị ID video nếu liên kết hợp lệ
if link:
    video_id = extract_video_id(link)
    if not video_id:
        st.error('Invalid YouTube URL')
    else:
        st.success(f'Video ID: {video_id}')
        comments = cmt_processing(video_id)
        for i in comments[:10]:
            st.text(i)

