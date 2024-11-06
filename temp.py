from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
from collections import Counter


# Định nghĩa tập dictionary của chat word mappings

def remove_stopwords(text):
    text = ' '.join([word for word in text.split() if word not in (stop)])
    return text


# Khởi tạo PorterStemmer


# Định nghĩa hàm apply_stemming để áp dụng quá trình stemming cho văn bản
def apply_stemming(text):
    words = word_tokenize(text)  # Tách văn bản thành danh sách các từ
    stemmed_words = [stemmer.stem(word) for word in words]  # Áp dụng stemming cho từng từ trong danh sách
    return ' '.join(stemmed_words)  # Kết hợp các từ sau khi stemming thành một chuỗi văn bản

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# Hàm lemmatization
def lemmatize_text(text):
    # Khởi tạo WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Tách từ
    tokens = word_tokenize(text)

    # Gắn thẻ từ loại
    tagged_tokens = nltk.pos_tag(tokens)

    # Lemmatization cho mỗi từ
    lemmatized_text = []
    for token, tag in tagged_tokens:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN
        lemmatized_text.append(lemmatizer.lemmatize(token, wordnet_pos))

    # Ghép các từ lại thành chuỗi
    return ' '.join(lemmatized_text)

#Định nghĩa các cặp từ điển
ner_dict = {"PERSON" : "[person]",
           "NORP": "[norp]",
           "FAC" : "[fac]",
           "ORG": "[org]",
           "GPE":"[gpe]",
           "LOC":"[loc]",
           "PRODUCT":"[product]",
           "EVENT":"[event]",
           "WORK_OF_ART": "[work_of_art]",
           "LAW":"[law]",
           "LANGUAGE":"[language]",
           "DATE":"[date]",
           "TIME":"[time]",
           "PERCENT":"[percent]",
           "MONEY":"[money]",
           "QUANTITY": "[quantity]",
           "ORDINAL": "[ordinal]",
           "CARDINAL": "[cardinal]"}

# Hàm thay thế tên riêng trong cột Text
def replace_entities(text_series):
    processed_texts = []
    for text in text_series:
        doc = nlp(text)
        # Thay thế từng thực thể có trong văn bản với nhãn tương ứng từ ner_dict
        for ent in doc.ents:
            text = text.replace(ent.text, ner_dict[ent.label_])
        processed_texts.append(text)
    return processed_texts




def tokenize(text):
  tokenizer = Tokenizer(num_words=60000)
  tokenizer.fit_on_texts(text)
  text_sequences = tokenizer.texts_to_sequences(text)
  return text_sequences

def padding(text_sequences):
  maxlen = max(len(tokens) for tokens in text_sequences)
  text_padded = pad_sequences(text_sequences, maxlen=maxlen, padding='post')
  return text_padded

from keras.models import load_model

import numpy as np

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
