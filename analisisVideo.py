from obtenerComentarios import obtener_comentarios
from limpiarTexto import limpiar_texto
from palabras_repetidas import obtener_palabras_repetidas
from sentimientos import polaridad_por_palabra
from tesauros import obtener_tesauros
from profealex import graficar_conceptos
from fastapi import FastAPI
import os
import shutil

app = FastAPI()

@app.get("/analizar/{VIDEO_ID}")
def analizar_video(VIDEO_ID: str):
  return procesamiento(VIDEO_ID)

def procesamiento(VIDEO_ID: str):
  archivos = obtener_comentarios(VIDEO_ID)
  print(f'Comentarios guardados en: {archivos["file_comentarios"]}')
  print(f'Usuarios guardados en: {archivos["file_usuarios"]}')
  print('Limpiando texto...')
  comentarios_limpios = limpiar_texto(archivos['file_comentarios'], archivos['file_usuarios'])
  print(f'Texto limpio guardado en: {comentarios_limpios} reformateado.json')
  print('Buscando palabras repetidas...')
  palabras_repetidas = obtener_palabras_repetidas(comentarios_limpios)
  print(f'Palabras repetidas guardadas en: {comentarios_limpios} palabras_repetidas.csv')
  print('Buscando polaridad por palabra...')
  polaridad_por_palabra(comentarios_limpios)
  print(f'Polaridad por palabra guardada en: {comentarios_limpios} polaridad.csv')
  print('Buscando tesauros...')
  obtener_tesauros(comentarios_limpios)
  print(f'Tesauros guardados en: {comentarios_limpios} conteos.json')
  print('Análisis de video completado.')
  palabra_mas_repetida = palabras_repetidas.head(10).index.tolist()
  print(f'Buscando conceptos relacionados a la palabra: {palabra_mas_repetida}')
  PALABRA_ELEGIDA = graficar_conceptos(palabra_mas_repetida, VIDEO_ID)
  # Mover todos los archivos generados a una carpeta
  # con el nombre del video
  # Crear carpeta si no existe

  carpeta = f'{VIDEO_ID}'
  if not os.path.exists(carpeta):
    os.makedirs(carpeta)
  else:
    # Si la carpeta ya existe, eliminarla y crear una nueva
    shutil.rmtree(carpeta)
    os.makedirs(carpeta)
  # Mover archivos a la carpeta
  shutil.move(archivos['file_comentarios'], carpeta)
  shutil.move(archivos['file_usuarios'], carpeta)
  shutil.move(f'{comentarios_limpios}', carpeta)
  shutil.move(f'{comentarios_limpios} palabras_repetidas.csv', carpeta)
  shutil.move(f'{comentarios_limpios} palabras_repetidas.png', carpeta)
  shutil.move(f'{comentarios_limpios} conteos.json', carpeta)
  shutil.move('graficas_tesauros', carpeta)
  shutil.move(f'{comentarios_limpios} polaridades detallado.json', carpeta)
  shutil.move(f'{comentarios_limpios} polaridades resumido.json', carpeta)
  shutil.move(f'{comentarios_limpios} polaridad.png', carpeta)
  shutil.move(f'{VIDEO_ID} request_log.json', carpeta)
  shutil.move(f'{VIDEO_ID} conceptos {PALABRA_ELEGIDA} relacionado.html', carpeta)
  shutil.move(f'{VIDEO_ID} conceptos {PALABRA_ELEGIDA} sin relacionar.html', carpeta)
  shutil.move(f'{VIDEO_ID} conceptos logs.json', carpeta)
  print(f'Archivos guardados en: {carpeta}')
  print('Fin del programa.')
  return _obtener_archivos_generados(VIDEO_ID)

@app.get("/archivos/{VIDEO_ID}")
def obtener_archivos_generados(VIDEO_ID: str):
  return _obtener_archivos_generados(VIDEO_ID)

def _obtener_archivos_generados(VIDEO_ID: str):
  import os
  import json
  import csv

  os.system('cls')

  if not os.path.exists(VIDEO_ID):
    return {
      "status": False,
      "msg": "No se encontraron archivos generados",
    }

  def _get_file(file_name):
    # Ingresa de la carpeta VIDEO_ID
    # y devuelve el nombre del archivo
    # con la ruta completa
    return os.path.join(VIDEO_ID, file_name)
  
  def get_file_json(file_name):
    with open(_get_file(file_name), 'r', encoding='utf-8') as file:
      return json.load(file)

  COMENTARIOS = get_file_json(f'{VIDEO_ID} comentarios.json')

  USUARIOS = get_file_json(f'{VIDEO_ID} usuarios.json')

  COMENTARIOS_LIMPIOS = get_file_json(f'{VIDEO_ID} comentarios.json reformateado.json')

  CONTEOS_TESAUROS = get_file_json(f'{VIDEO_ID} comentarios.json reformateado.json conteos.json')

  def get_csv_to_json(file_name):
    # Convierte el archivo csv a json
    # y devuelve el json
    with open(_get_file(file_name), 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      data = [row for row in reader]
    return data
  
  PALABRAS_REPETIDAS = get_csv_to_json(f'{VIDEO_ID} comentarios.json reformateado.json palabras_repetidas.csv')

  POLARIDAD_DETALLADA = get_file_json(f'{VIDEO_ID} comentarios.json reformateado.json polaridades detallado.json')

  POLARIDAD_RESUMIDO = get_file_json(f'{VIDEO_ID} comentarios.json reformateado.json polaridades resumido.json')

  CONCEPTOS_OPEN_ALEX = get_file_json(f'{VIDEO_ID} conceptos logs.json')

  return {
    "status": True,
    "msg": "Análisis de video completado",
    "comentarios": COMENTARIOS,
    "usuarios": USUARIOS,
    "comentarios_limpios": COMENTARIOS_LIMPIOS,
    "palabras_repetidas": PALABRAS_REPETIDAS,
    "polaridad_detallada": POLARIDAD_DETALLADA,
    "polaridad_resumido": POLARIDAD_RESUMIDO,
    "conteos_tesauros": CONTEOS_TESAUROS,
    "conceptos_open_alex": CONCEPTOS_OPEN_ALEX,
  }

# if __name__ == '__main__':
  # procesamiento('Ncwi1DGAGkk')
  # print(obtener_archivos_generados('Ncwi1DGAGkk'))

if __name__ == '__main__':
  import uvicorn
  uvicorn.run('analisisVideo:app', reload=True)