import nltk
from googleapiclient.discovery import build

import spacy
# Load the spaCy model
import spacy
st.text(spacy.util.get_package_path("en_core_web_sm"))

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
