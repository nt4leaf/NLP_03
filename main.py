import streamlit as st
import comments_youtube
import re

 # Hàm để trích xuất ID video từ liên kết YouTube
def extract_video_id(url):
    # Sử dụng regex để tìm ID video
    video_id = re.search(r'(?<=v=)[^&#]+', url)
    if not video_id:
        video_id = re.search(r'(?<=be/)[^&#]+', url)
    return video_id.group(0) if video_id else None

def cmt_processing(video_id):
    comments = comments_youtube.video_comments(video_id)
    #clear_text = comments_youtube.text_processing(comments)
    # clear_text_padded = comments_youtube.padding(tokenize(clear_text))
    return comments

# Giao diện Streamlit
st.title('YouTube Video ID Extractor')

# Nhập liên kết YouTube
url = st.text_input('Enter YouTube URL')

# Hiển thị ID video nếu liên kết hợp lệ
if url:
    video_id = extract_video_id(url)
    if not video_id:
        st.error('Invalid YouTube URL')
    else:
        st.success(f'Video ID: {video_id}')
        comments = cmt_processing(video_id)
        for i in comments:
            st.text(i)

