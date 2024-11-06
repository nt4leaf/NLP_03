import gdown
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from sub2 import video_comments
from sub3 import text_processing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

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
    check, comments = video_comments(video_id)
    if not check:
        return 0
    clear_text = text_processing(comments)
    clear_text_padded = padding(tokenize(clear_text))
    file_id = '1peNnSykGJUtQpq9Y12Ax-xP6T4sgy2bd'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'best_model_128.keras'
    gdown.download(url, output, quiet=False)
    model = tf.keras.models.load_model('best_model_128.keras')

    y_pred = model.predict(clear_text_padded)
    y_pred = np.argmax(y_pred, axis=1)
    
    emote_predict = [emote_mapping[i] for i in y_pred]
    df_comments = pd.DataFrame({
        'Comment': comments,
        'Emotion': emote_predict
    })
    emote_counts = Counter(emote_predict)
    df_emote_counts = pd.DataFrame.from_dict(emote_counts, orient='index', columns=['Count'])
    df_emote_counts = df_emote_counts.rename_axis('Emotion').reset_index()
    df_emote_counts = df_emote_counts[['Emotion', 'Count']]

    st.text("Thống kê nhãn bình luận của video:")
    st.dataframe(df_emote_counts, width=400, height=500)
    st.text("\nNhãn của các bình luận:")
    st.dataframe(df_comments, width=400, height=800)
    return 1



