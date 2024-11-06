from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def video_comments(video_id):
    api_key = 'AIzaSyBP5BExPx1lN_wlS8uiITi1WKpBnQ9G_ig'
    replies = []
    comments = []
    youtube = build('youtube', 'v3', developerKey=api_key)
    #video_response=youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

    try:
        video_response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()
    except HttpError as e:
        return 0, []

    while video_response:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            replycount = item['snippet']['totalReplyCount']

            if replycount>0:
                for reply in item['replies']['comments']:
                    reply = reply['snippet']['textDisplay']
                    replies.append(reply)
            replies = []

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                      pageToken = video_response['nextPageToken']
                ).execute()
        else:
            break
    return 1, comments