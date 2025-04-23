from obtenerComentarios import obtener_comentarios
from limpiarTexto import limpiar_texto
from palabras_repetidas import obtener_palabras_repetidas
from sentimientos import polaridad_por_palabra
from tesauros import obtener_tesauros
from profealex import graficar_conceptos
from os import system
import platform

def limpiar_pantalla():
  system('cls' if platform.system() == 'Windows' else 'clear')

if __name__ == '__main__':
  limpiar_pantalla()
  VIDEO_ID = input('Introduce el ID del video: ')
  archivos = obtener_comentarios(VIDEO_ID)
  print(f'Comentarios guardados en: {archivos["file_comentarios"]}')
  print(f'Usuarios guardados en: {archivos["file_usuarios"]}')
  print('Limpiando texto...')
  comentarios_limpios = limpiar_texto(archivos['file_comentarios'], archivos['file_usuarios'])
  print(f'Texto limpio guardado en: {archivos["file_comentarios"]} reformateado.json')
  print('Buscando palabras repetidas...')
  palabras_repetidas = obtener_palabras_repetidas(archivos['file_comentarios'])
  print(f'Palabras repetidas guardadas en: {archivos["file_comentarios"]} palabras_repetidas.csv')
  print('Buscando polaridad por palabra...')
  polaridad_por_palabra(archivos['file_comentarios'])
  print(f'Polaridad por palabra guardada en: {archivos["file_comentarios"]} polaridad.csv')
  print('Buscando tesauros...')
  obtener_tesauros(archivos['file_comentarios'])
  print(f'Tesauros guardados en: {archivos["file_comentarios"]} conteos.json')
  print('Análisis de video completado.')
  palabra_mas_repetida = palabras_repetidas.head(10).index.tolist()
  print(f'Buscando conceptos relacionados a la palabra: {palabra_mas_repetida}')
  PALABRA_ELEGIDA = graficar_conceptos(palabra_mas_repetida, VIDEO_ID)
  # Mover todos los archivos generados a una carpeta
  # con el nombre del video
  # Crear carpeta si no existe
  import os
  import shutil
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
  shutil.move(f'{archivos["file_comentarios"]} reformateado.json', carpeta)
  shutil.move(f'{archivos["file_comentarios"]} palabras_repetidas.csv', carpeta)
  shutil.move(f'{archivos["file_comentarios"]} conteos.json', carpeta)
  shutil.move(f'{archivos["file_comentarios"]} polaridades detallado.json', carpeta)
  shutil.move(f'{archivos["file_comentarios"]} polaridades resumido.json', carpeta)
  shutil.move(f'{VIDEO_ID} request_log.json', carpeta)
  shutil.move(f'{VIDEO_ID} conceptos {PALABRA_ELEGIDA} relacionado.html', carpeta)
  shutil.move(f'{VIDEO_ID} conceptos {PALABRA_ELEGIDA} sin relacionar.html', carpeta)
  print(f'Archivos guardados en: {carpeta}')
  print('Fin del programa.')
