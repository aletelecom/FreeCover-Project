import pandas as pd
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEVELOPER_KEY = '[DEVELOPER_KEY]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULTS = 100 # Maximum number of comments to retrieve per video

def get_all_video_comments(channel_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Retrieve the channel's videos
    videos = []
    next_page_token = None

    while True:
        videos_request = youtube.search().list(
            part="id",
            channelId=channel_id,
            type='video',
            maxResults=500,
            pageToken=next_page_token
        )
        videos_response = videos_request.execute()
        videos += videos_response['items']

        next_page_token = videos_response.get('nextPageToken')

        if not next_page_token:
            break

    # Create a list to store the comments
    comments = []

    # Loop through each video and retrieve its comments
    for video in videos:
        video_id = video['id']['videoId']
        video_request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()

        # Retrieve the video's information
        video_title = video_response['items'][0]['snippet']['title']
        video_description = video_response['items'][0]['snippet']['description']
        video_date = video_response['items'][0]['snippet']['publishedAt']

        # Retrieve the comments for the video
        try:
            comments_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=MAX_RESULTS
            )
            comments_response = comments_request.execute()

            # Loop through each comment and add it to the list
            while comments_response.get("items"):
                for comment in comments_response['items']:
                    comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    comment_date = comment['snippet']['topLevelComment']['snippet']['publishedAt']

                    # Add the comment to the list
                    comments.append({
                        'video_id': video_id,
                        'video_title': video_title,
                        'video_description': video_description,
                        'video_date': video_date,
                        'comment_text': comment_text,
                        'comment_date': comment_date
                    })

                # Check if there are more comments for this video
                if 'nextPageToken' in comments_response:
                    comments_request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=MAX_RESULTS,
                        pageToken=comments_response['nextPageToken']
                    )
                    comments_response = comments_request.execute()
                else:
                    break

        except HttpError as error:
            print(f"An error occurred while retrieving comments for video {video_id}: {error}")

    # Create a pandas DataFrame from the list of comments
    comments_df = pd.DataFrame(comments)

    return comments_df



def __main__():
	CHANNEL_ID = 'UCnntVqOb0AOzjDE13PjHeRw'
	comments_df = get_all_video_comments(CHANNEL_ID)
	
	comentarios_path = os.path.join('..','Comentarios')
	file_name = 'Comentarios-FreeCover(v2).xlsx'
	file_path = os.path.join(comentarios_path, file_name)
	
	print('Guardando datos...')
	
	comments_df.to_excel(file_path)
	print('Proceso finalizado con exito.')


# Call the main function
if __name__ == '__main__':
	__main__()
