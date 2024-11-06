from googleapiclient.discovery import build
import subprocess
import nltk
import streamlit as st
st.text(nltk.data.path)
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
stop = stopwords.words('english')

stemmer = PorterStemmer()

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

spacy_install_output = run_cmd("python -m spacy download en_core_web_sm")

# Sử dụng stopwords của NLTK


api_key = 'AIzaSyBP5BExPx1lN_wlS8uiITi1WKpBnQ9G_ig'

def video_comments(video_id):
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

# Định nghĩa hàm apply_stemming để áp dụng quá trình stemming cho văn bản
def apply_stemming(text):
    ps = PorterStemmer()
    words = word_tokenize(text)  # Tách văn bản thành danh sách các từ
    stemmed_words = [ps.stem(word) for word in words]  # Áp dụng stemming cho từng từ trong danh sách
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
    #if isinstance(i, str):
    #  i = apply_stemming(i)
    #  i = lemmatize_text(i)
    clear_text.append(i)
    # Trả về clear_text sau khi đã thay các cụm từ riêng bằng cụm từ cố định
  return clear_text
