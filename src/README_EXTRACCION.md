# Obtener Comentarios de YouTube

Este programa en Python te permite obtener comentarios de videos de YouTube utilizando la API de Google. Puedes proporcionar un ID de canal de YouTube y el programa recuperará todos los videos del canal, junto con sus respectivos comentarios. Los comentarios se guardarán en un archivo Excel (.xlsx) para su posterior análisis.

## Requisitos previos

Antes de utilizar este programa, asegúrate de tener instalado lo siguiente:
- Python 3.x: https://www.python.org/downloads/
- Biblioteca pandas: Ejecuta `pip install pandas` para instalarla.

Además, necesitarás una clave de desarrollador válida de la API de Google para realizar solicitudes a la API de YouTube. Asegúrate de tener tu clave de desarrollador lista para utilizarla en el código.

## Uso

1. Clona este repositorio en tu máquina local.
2. Coloca la clave de desarrollador en la variable `DEVELOPER_KEY` en el archivo `free_cover_comments.py`.
3. Abre una terminal o línea de comandos y navega hasta la carpeta "src" del repositorio clonado.
4. Ejecuta el siguiente comando:

python free_cover_comments.py

5. El programa comenzará a recuperar los videos del canal y sus comentarios. Verás mensajes de progreso en la terminal.
6. Una vez completado, el programa guardará los comentarios en un archivo Excel llamado "Comentarios-FreeCover.xlsx".
7. ¡Listo! Ahora puedes abrir el archivo Excel para ver los comentarios obtenidos y realizar cualquier análisis adicional que desees.

## Salida del código

El programa generará un archivo Excel llamado "Comentarios-FreeCover(v2).xlsx" que contendrá la siguiente información para cada comentario:

- `video_id`: ID del video al que pertenece el comentario.
- `video_titulo`: Título del video.
- `video_descripcion`: Descripción del video.
- `video_fecha`: Fecha de publicación del video.
- `texto_comentario`: Texto del comentario.
- `fecha_comentario`: Fecha de publicación del comentario.

## Notas

- Si ocurre algún error durante la recuperación de comentarios, se mostrará un mensaje en la terminal indicando el problema.
- Asegúrate de respetar las políticas y condiciones de uso de la API de Google y de YouTube al utilizar este programa.
- Este programa está destinado solo para fines educativos y de aprendizaje.

¡Disfruta explorando y analizando los comentarios de YouTube con este programa!