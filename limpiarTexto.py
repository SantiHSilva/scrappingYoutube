import json
import re

ARCHIVO = "1744989070 comentarios.json"
LISTA_DE_EXCLUSION_ARCHIVO = "1744989070 usuarios.json"
REEMPLAZOS = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ñ": "n",
    "ü": "u",
    "¿": "",
    "?": "",
    "!": "",
    "¡": "",
    ".": "",
    ",": "",
    ";": "",
    ":": "",
    "\n": " ",
}

def limpiar_texto(texto):
    texto = texto.lower()
    texto = ''.join(e for e in texto if e.isalnum() or e.isspace())
    for clave, valor in REEMPLAZOS.items():
        texto = texto.replace(clave, valor)
    return texto

with open(ARCHIVO, 'r', encoding='utf-8') as f:
    comentarios = json.load(f)
    NUEVOS_COMENTARIOS = []
    for comentario in comentarios:
        filtrado = limpiar_texto(comentario)
        NUEVOS_COMENTARIOS.append(filtrado)
    comentarios = NUEVOS_COMENTARIOS

with open(LISTA_DE_EXCLUSION_ARCHIVO, 'r', encoding='utf-8') as f:
    lista_de_exclusion = json.load(f)
    lista_de_exclusion = [limpiar_texto(usuario) for usuario in lista_de_exclusion]

def reemplazar_usuarios(comentarios, lista_de_exclusion):
    NUEVOS_COMENTARIOS = []
    for comentario in comentarios:
        for usuario in lista_de_exclusion:
            comentario = comentario.replace(usuario, "")
        NUEVOS_COMENTARIOS.append(comentario)
    return NUEVOS_COMENTARIOS

NUEVOS_COMENTARIOS = reemplazar_usuarios(comentarios, lista_de_exclusion)

def trim_and_filter_comments(nuevos_comentarios):
    # strip y remover vacíos
    NUEVOS_COMENTARIOS = []
    for comentario in nuevos_comentarios:
        comentario = comentario.strip()
        if comentario:
            #remove extra spaces in between
            comentario = re.sub(r'\s+', ' ', comentario)
            # remove punctuation
            comentario = re.sub(r'[^\w\s]', '', comentario)
            NUEVOS_COMENTARIOS.append(comentario)
    return NUEVOS_COMENTARIOS

NUEVOS_COMENTARIOS = trim_and_filter_comments(NUEVOS_COMENTARIOS)

# Guardamos los resultados en un archivo JSON
with open(f'{ARCHIVO} reformateado.json', 'w', encoding='utf-8') as f:
    json.dump(NUEVOS_COMENTARIOS, f, ensure_ascii=False, indent=4)