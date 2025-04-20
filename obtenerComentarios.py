from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import json

load_dotenv()

KEY = os.getenv('YOUTUBE_KEY')
API_VERSION = 'v3'
YOUTUBE = build('youtube', API_VERSION, developerKey=KEY)
MAX_RESULTS = 100

def obtener_comentarios(VIDEO_ID):
  comentarios = YOUTUBE.commentThreads()
  request = comentarios.list(
    part="replies,snippet,id",
    videoId=VIDEO_ID,
    maxResults=MAX_RESULTS,
  )

  RESULTADOS = [] # Lista para almacenar los resultados
  REQUEST_LOG = []
  USUARIOS = []

  while request is not None:
    pagina = request.execute()
    REQUEST_LOG.append(pagina) # Guardamos la página en el log

    COMENTARIOS_FORMATTED = []

    for item in pagina['items']:
      keys = item.keys()
      if('snippet' in keys and 'topLevelComment' in item['snippet'].keys()):
        COMENTARIOS_FORMATTED.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
        USUARIOS.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
      
      if('replies' in keys):
        for reply in item['replies']['comments']:
          if(reply['snippet']['textOriginal']):
            COMENTARIOS_FORMATTED.append(reply['snippet']['textOriginal'])
            USUARIOS.append(reply['snippet']['authorDisplayName'])

    RESULTADOS += COMENTARIOS_FORMATTED

    request = comentarios.list_next(request, pagina)

  print(f'Se han encontrado {len(RESULTADOS)} comentarios.')

  FILE_COMENTARIOS = f'{VIDEO_ID} comentarios.json'
  FILE_USUARIOS = f'{VIDEO_ID} usuarios.json'

  # guardamos los resultados en un archivo JSON
  with open(f'{FILE_COMENTARIOS}', 'w', encoding='utf-8') as f:
    json.dump(RESULTADOS, f, ensure_ascii=False, indent=4)

  with open(f'{VIDEO_ID} request_log.json', 'w', encoding='utf-8') as f:
    json.dump(REQUEST_LOG, f, ensure_ascii=False, indent=4)

  with open(f'{FILE_USUARIOS}', 'w', encoding='utf-8') as f:
    json.dump(USUARIOS, f, ensure_ascii=False, indent=4)

  return {
    'file_comentarios': FILE_COMENTARIOS,
    'file_usuarios': FILE_USUARIOS,
  }

if __name__ == '__main__':
  VIDEO_ID = 'Ncwi1DGAGkk'
  archivos = obtener_comentarios(VIDEO_ID)
  print(f'Comentarios guardados en: {archivos["file_comentarios"]}')
  print(f'Usuarios guardados en: {archivos["file_usuarios"]}')