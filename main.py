import comments_youtube
import nltk
import streamlit as st
st.text(nltk.data.path)
import re
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punktab')
nltk.download('averaged_perceptron_tagger')
 # Hàm để trích xuất ID video từ liên kết YouTube
def extract_video_id(url):
    # Sử dụng regex để tìm ID video
    video_id = re.search(r'(?<=v=)[^&#]+', url)
    if not video_id:
        video_id = re.search(r'(?<=be/)[^&#]+', url)
    return video_id.group(0) if video_id else None

def cmt_processing(video_id):
    comment = comments_youtube.video_comments(video_id)
    clear_text = comments_youtube.text_processing(comment)
    # clear_text_padded = comments_youtube.padding(tokenize(clear_text))
    return clear_text

# Giao diện Streamlit
st.title('YouTube Video ID Extractor')

# Nhập liên kết YouTube
link = st.text_input('Enter YouTube URL')

# Hiển thị ID video nếu liên kết hợp lệ
if link:
    vid_id = extract_video_id(link)
    if not vid_id:
        st.error('Invalid YouTube URL')
    else:
        st.success(f'Video ID: {vid_id}')
        comments = cmt_processing(vid_id)
        for i in comments:
            st.text(i)

