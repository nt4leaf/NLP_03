import nltk
from googleapiclient.discovery import build
import streamlit as st
import streamlit as st
import subprocess
import nltk

# Hàm để chạy lệnh CMD
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# Chạy lệnh cài đặt môi trường
st.write("Đang cài đặt môi trường...")

# Cài đặt mô hình spaCy
spacy_install_output = run_cmd("python -m spacy download en_core_web_sm")
st.text_area("Cài đặt spaCy:", spacy_install_output)

# Tải xuống dữ liệu NLTK
nltk.download('stopwords')

# Kiểm tra cài đặt
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    st.success("Mô hình 'en_core_web_sm' đã được cài đặt thành công.")
except OSError:
    st.error("Không thể cài đặt mô hình 'en_core_web_sm'.")

# Sử dụng stopwords của NLTK
stop = nltk.corpus.stopwords.words('english')
st.text(f"Stopwords: {stop[:10]}")  # Hiển thị 10 stopwords đầu tiên làm ví dụ

# Giao diện Streamlit
st.title("Ứng dụng Streamlit với cài đặt môi trường tự động")

from nltk.corpus import stopwords
stop = stopwords.words('english')

from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

api_key = 'AIzaSyBP5BExPx1lN_wlS8uiITi1WKpBnQ9G_ig'

def video_comments(video_id):
    # empty list for storing reply
    replies = []
    comments = []

    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    # retrieve youtube video results
    video_response=youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

    # iterate video response
    while video_response:

        # extracting required info
        # from each result object
        for item in video_response['items']:

            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']

            # if reply is there
            if replycount>0:

                # iterate through all reply
                for reply in item['replies']['comments']:

                    # Extract reply
                    reply = reply['snippet']['textDisplay']

                    # Store reply is list
                    replies.append(reply)

            # empty reply list
            replies = []

        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                      pageToken = video_response['nextPageToken']
                ).execute()
        else:
            break

    return comments
