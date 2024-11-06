from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sub2 import video_comments
from sub3 import text_processing
import numpy as np
import streamlit as st
import requests
import tensorflow as tf


def tokenize(text):
  tokenizer = Tokenizer(num_words=60000)
  tokenizer.fit_on_texts(text)
  text_sequences = tokenizer.texts_to_sequences(text)
  return text_sequences

def padding(text_sequences):
  maxlen = max(len(tokens) for tokens in text_sequences)
  text_padded = pad_sequences(text_sequences, maxlen=maxlen, padding='post')
  return text_padded


def model_pred(video_id):
    comments = video_comments(video_id)
    st.text("success_1")
    clear_text = text_processing(comments)
    st.text("success_2")
    clear_text_padded = padding(tokenize(clear_text))
    st.text("success_3")
    """
    # Load model
    url = ''
    r = requests.get(url, allow_redirects=True)
    open('.h5', 'wb').write(r.content)
    model = tf.keras.models.load_model('.h5')
    st.text("success_4")

    # Predict
    #y_pred = model.predict(clear_text_padded)
    #y_pred = np.argmax(y_pred, axis=1)

    
    emote_predict = [emote_mapping[i] for i in y_pred]
    df_comments = pd.DataFrame({
        'Comment': comments,
        'Emotion': emote_predict
    })
    emote_counts = Counter(emote_predict)
    df_emote_counts = pd.DataFrame.from_dict(emote_counts, orient='index', columns=['Count'])
    df_emote_counts = df_emote_counts.rename_axis('Emotion').reset_index()
    df_emote_counts = df_emote_counts[['Emotion', 'Count']]

    print("Thống kê nhãn bình luận của video:")
    print(df_emote_counts)

    print("\nNhãn của các bình luận:")
    print(df_comments)
    """




"""
from keras.models import load_model
import numpy as np
import pandas as pd

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

from collections import Counter
"""

