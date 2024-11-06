from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sub2 import video_comments
from sub3 import text_processing
import streamlit as st
import gdown
import tensorflow as tf
import numpy as np
import pandas as pd

from collections import Counter

def tokenize(text):
  tokenizer = Tokenizer(num_words=60000)
  tokenizer.fit_on_texts(text)
  text_sequences = tokenizer.texts_to_sequences(text)
  return text_sequences

def padding(text_sequences):
  maxlen = max(len(tokens) for tokens in text_sequences)
  text_padded = pad_sequences(text_sequences, maxlen=maxlen, padding='post')
  return text_padded

# Định nghĩa từ điển ánh xạ
emote_mapping = {
    0: 'hate',
    1: 'neutral',
    2: 'anger',
    3: 'love',
    4: 'worry',
    5: 'relief',
    6: 'happiness',
    7: 'fun',
    8: 'empty',
    9: 'enthusiasm',
    10: 'sadness',
    11: 'surprise',
    12: 'boredom'
}

def model_pred(video_id):
    comments = video_comments(video_id)
    st.text("success_1: Trch xuất comments thành công")
    clear_text = text_processing(comments)
    st.text("success_2: Tiền xử lý thành công")
    clear_text_padded = padding(tokenize(clear_text))
    st.text("success_3: Padding dữ liệu thành công")
    # ID của file từ URL chia sẻ của Google Drive
    file_id = '1RJpFlDTmuNRWbgDgpZWUm_XtOcPmh-Ec'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'best_model_128.keras'
    gdown.download(url, output, quiet=False)
    # Tải mô hình
    model = tf.keras.models.load_model('best_model_128.keras')
    st.text("success_4: Load model thành công")
    # Predict
    y_pred = model.predict(clear_text_padded)
    y_pred = np.argmax(y_pred, axis=1)
    
    emote_predict = [emote_mapping[i] for i in y_pred]
    df_comments = pd.DataFrame({
        'Comment': comments,
        'Emotion': emote_predict
    })
    st.dataframe(df_comments)

    emote_counts = Counter(emote_predict)
    df_emote_counts = pd.DataFrame.from_dict(emote_counts, orient='index', columns=['Count'])
    df_emote_counts = df_emote_counts.rename_axis('Emotion').reset_index()
    df_emote_counts = df_emote_counts[['Emotion', 'Count']]

    st.text("Thống kê nhãn bình luận của video:")
    st.dataframe(df_emote_counts)

    st.text("\nNhãn của các bình luận:")
    st.text(df_comments)




