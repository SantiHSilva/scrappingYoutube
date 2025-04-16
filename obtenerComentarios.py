from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv()

KEY = os.getenv('YOUTUBE_KEY')
API_VERSION = 'v3'
YOUTUBE = build('youtube', API_VERSION, developerKey=KEY)
MAX_RESULTS = 100

comentarios = YOUTUBE.commentThreads()
request = comentarios.list(
  part="replies,snippet,id",
  videoId="Ncwi1DGAGkk",
  maxResults=MAX_RESULTS,
)

RESULTADOS = [] # Lista para almacenar los resultados
contador = 0
REQUEST_LOG = []

while request is not None:
  pagina = request.execute()
  REQUEST_LOG.append(pagina) # Guardamos la página en el log

  COMENTARIOS_FORMATTED = []

  for item in pagina['items']:
    # if(item['snippet']['topLevelComment']['snippet']['textDisplay']):
    keys = item.keys()
    if('snippet' in keys and 'topLevelComment' in item['snippet'].keys()):
      COMENTARIOS_FORMATTED.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    
    if('replies' in item.keys()):
      for reply in item['replies']['comments']:
        if(reply['snippet']['textDisplay']):
          COMENTARIOS_FORMATTED.append(reply['snippet']['textDisplay'])

  RESULTADOS += COMENTARIOS_FORMATTED # Agregamos los comentarios a la lista de resultados

  request = comentarios.list_next(request, pagina)
  contador += 1 # Incrementamos el contador
  # input()


# print(f'{RESULTADOS}')
print(f'Se han encontrado {len(RESULTADOS)} comentarios.')

timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))

# guardamos
# los resultados en un archivo JSON
with open(f'{timestamp} comentarios.json', 'w', encoding='utf-8') as f:
  json.dump(RESULTADOS, f, ensure_ascii=False, indent=4)

with open(f'{timestamp} request_log.json', 'w', encoding='utf-8') as f:
  json.dump(REQUEST_LOG, f, ensure_ascii=False, indent=4)