import pandas as pd
from datetime import datetime
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEVELOPER_KEY = '[DEVELOPER_KEY]' # Aquí deben colocar la clave de desarrollador de la API de Google
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULTS = 100 # Número máximo de comentarios a recuperar por video

def obtener_todos_los_comentarios_de_video(id_canal):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Recuperar los videos del canal
    videos = []
    next_page_token = None

    while True:
        videos_request = youtube.search().list(
            part="id",
            channelId=id_canal,
            type='video',
            maxResults=500,
            pageToken=next_page_token
        )
        videos_response = videos_request.execute()
        videos += videos_response['items']

        next_page_token = videos_response.get('nextPageToken')

        if not next_page_token:
            break

    # Crear una lista para almacenar los comentarios
    comentarios = []

    # Recorrer cada video y recuperar sus comentarios
    for video in videos:
        video_id = video['id']['videoId']
        video_request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()

        # Recuperar la información del video
        video_titulo = video_response['items'][0]['snippet']['title']
        video_descripcion = video_response['items'][0]['snippet']['description']
        video_fecha = video_response['items'][0]['snippet']['publishedAt']

        # Recuperar los comentarios para el video
        try:
            comentarios_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=MAX_RESULTS
            )
            comentarios_response = comentarios_request.execute()

            # Recorrer cada comentario y agregarlo a la lista
            while comentarios_response.get("items"):
                for comentario in comentarios_response['items']:
                    texto_comentario = comentario['snippet']['topLevelComment']['snippet']['textDisplay']
                    fecha_comentario = comentario['snippet']['topLevelComment']['snippet']['publishedAt']

                    # Agregar el comentario a la lista
                    comentarios.append({
                        'video_id': video_id,
                        'video_titulo': video_titulo,
                        'video_descripcion': video_descripcion,
                        'video_fecha': video_fecha,
                        'texto_comentario': texto_comentario,
                        'fecha_comentario': fecha_comentario
                    })

                # Verificar si hay más comentarios para este video
                if 'nextPageToken' in comentarios_response:
                    comentarios_request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=MAX_RESULTS,
                        pageToken=comentarios_response['nextPageToken']
                    )
                    comentarios_response = comentarios_request.execute()
                else:
                    break

        except HttpError as error:
            print(f"Ocurrió un error al recuperar los comentarios del video {video_id}: {error}")

    # Crear un DataFrame de pandas a partir de la lista de comentarios
    comentarios_df = pd.DataFrame(comentarios)

    return comentarios_df

def __main__():
    CHANNEL_ID = 'UCnntVqOb0AOzjDE13PjHeRw'
    comentarios_df = obtener_todos_los_comentarios_de_video(CHANNEL_ID)
    
    comentarios_path = os.path.join('..','Comentarios')
    file_name = 'Comentarios-FreeCover(v2).xlsx'
    file_path = os.path.join(comentarios_path, file_name)
    
    print('Guardando datos...')

    def remove_timezone(dt):
        """Remove timezone information from a datetime object."""
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt

    comentarios_df['video_date'] = comentarios_df['video_date'].apply(remove_timezone)
    comentarios_df['comment_date'] = comentarios_df['video_date'].apply(remove_timezone)
    
    comentarios_df.to_excel(file_path)
    print('Proceso finalizado con éxito.')

# Llamar a la función principal
if __name__ == '__main__':
    __main__()