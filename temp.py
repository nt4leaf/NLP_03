from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
from collections import Counter


# Định nghĩa tập dictionary của chat word mappings
chat_words = {
    "AFAIK": "As Far As I Know",
    "AFK": "Away From Keyboard",
    "ASAP": "As Soon As Possible",
    "ATK": "At The Keyboard",
    "A3": "Anytime, Anywhere, Anyplace",
    "BAK": "Back At Keyboard",
    "BBL": "Be Back Later",
    "BBS": "Be Back Soon",
    "BFN": "Bye For Now",
    "B4N": "Bye For Now",
    "BRB": "Be Right Back",
    "BRT": "Be Right There",
    "BTW": "By The Way",
    "B4": "Before",
    "B4N": "Bye For Now",
    "CU": "See You",
    "CUL8R": "See You Later",
    "CYA": "See You",
    "FAQ": "Frequently Asked Questions",
    "FC": "Fingers Crossed",
    "FWIW": "For What It's Worth",
    "FYI": "For Your Information",
    "GAL": "Get A Life",
    "GG": "Good Game",
    "GN": "Good Night",
    "GMTA": "Great Minds Think Alike",
    "GR8": "Great!",
    "G9": "Genius",
    "IC": "I See",
    "ICQ": "I Seek you (also a chat program)",
    "ILU": "ILU: I Love You",
    "IMHO": "In My Honest/Humble Opinion",
    "IMO": "In My Opinion",
    "IOW": "In Other Words",
    "IRL": "In Real Life",
    "KISS": "Keep It Simple, Stupid",
    "LDR": "Long Distance Relationship",
    "LMAO": "Laugh My A.. Off",
    "LOL": "Laughing Out Loud",
    "LTNS": "Long Time No See",
    "L8R": "Later",
    "MTE": "My Thoughts Exactly",
    "M8": "Mate",
    "NRN": "No Reply Necessary",
    "OIC": "Oh I See",
    "PITA": "Pain In The A..",
    "PRT": "Party",
    "PRW": "Parents Are Watching",
    "QPSA?": "Que Pasa?",
    "ROFL": "Rolling On The Floor Laughing",
    "ROFLOL": "Rolling On The Floor Laughing Out Loud",
    "ROTFLMAO": "Rolling On The Floor Laughing My A.. Off",
    "SK8": "Skate",
    "STATS": "Your sex and age",
    "ASL": "Age, Sex, Location",
    "THX": "Thank You",
    "TTFN": "Ta-Ta For Now!",
    "TTYL": "Talk To You Later",
    "U": "You",
    "U2": "You Too",
    "U4E": "Yours For Ever",
    "WB": "Welcome Back",
    "WTF": "What The F...",
    "WTG": "Way To Go!",
    "WUF": "Where Are You From?",
    "W8": "Wait...",
    "7K": "Sick:-D Laugher",
    "TFW": "That feeling when",
    "MFW": "My face when",
    "MRW": "My reaction when",
    "IFYP": "I feel your pain",
    "TNTL": "Trying not to laugh",
    "JK": "Just kidding",
    "IDC": "I don't care",
    "ILY": "I love you",
    "IMU": "I miss you",
    "ADIH": "Another day in hell",
    "ZZZ": "Sleeping, bored, tired",
    "WYWH": "Wish you were here",
    "TIME": "Tears in my eyes",
    "BAE": "Before anyone else",
    "FIMH": "Forever in my heart",
    "BSAAW": "Big smile and a wink",
    "BWL": "Bursting with laughter",
    "BFF": "Best friends forever",
    "CSL": "Can't stop laughing"
}

# Hàm thay thế các từ viết tắt trong chat bằng dạng đầy đủ
def replace_chat_words(text):
    words = text.split()  # Tách văn bản thành các từ riêng biệt
    for i, word in enumerate(words):  # Lặp qua từng từ trong văn bản
        if word.lower() in chat_words:  # Kiểm tra nếu từ viết tắt nằm trong từ điển chat_words
            words[i] = chat_words[word.lower()]  # Thay thế từ viết tắt bằng dạng đầy đủ
    return ' '.join(words)  # Ghép các từ lại thành văn bản đã được thay thế

def remove_stopwords(text):
    text = ' '.join([word for word in text.split() if word not in (stop)])
    return text


# Khởi tạo PorterStemmer
stemmer = PorterStemmer()

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

def text_processing(comments):
  clear_text = []
  for i in comments:
    # Loại bỏ thẻ HTML
    i = re.sub('<[^<]+?>', '', i)
    # Loại bỏ dường dẫn
    i = re.sub(r'http\S+', '', i)
    # Thay thế chat words bằng cụm từ đầy đủ
    i = replace_chat_words(str(i))
    # Loại bỏ ký tự không phải chữ cái
    i = re.sub(r'[^a-zA-Z\s]', '', i)
    # Loại bỏ stopwords
    i = remove_stopwords(i)
    # Đồng bộ văn bản về chữ thường
    i = i.lower()
    # Loại bỏ số
    i = re.sub(r'\d+', '', i)
    # Loại bỏ khoảng trắng thừa
    i = re.sub(r'\s+', ' ', i)
    i = i.strip()
    # Loại bỏ ký tự đặc biệt
    i = re.sub(r'[^\w\s]', '', i)
    # Stemming và Lemmatization
    if isinstance(i, str):
      i = apply_stemming(i)
      i = lemmatize_text(i)
    clear_text.append(i)
    # Trả về clear_text sau khi đã thay các cụm từ riêng bằng cụm từ cố định
  return replace_entities(clear_text)



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
