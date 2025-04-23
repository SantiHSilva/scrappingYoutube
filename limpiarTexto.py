import json
import re

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

def _limpiar_texto(texto):
    texto = texto.lower()
    texto = ''.join(e for e in texto if e.isalnum() or e.isspace())
    for clave, valor in REEMPLAZOS.items():
        texto = texto.replace(clave, valor)
    return texto

def _reemplazar_usuarios(comentarios, lista_de_exclusion):
    NUEVOS_COMENTARIOS = []
    for comentario in comentarios:
        for usuario in lista_de_exclusion:
            comentario = comentario.replace(usuario, "")
        NUEVOS_COMENTARIOS.append(comentario)
    return NUEVOS_COMENTARIOS

def _trim_and_filter_comments(nuevos_comentarios):
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

def limpiar_texto(archivo, lista_exclusion):
    with open(archivo, 'r', encoding='utf-8') as f:
        comentarios = json.load(f)
        NUEVOS_COMENTARIOS = []
        for comentario in comentarios:
            filtrado = _limpiar_texto(comentario)
            NUEVOS_COMENTARIOS.append(filtrado)
        comentarios = NUEVOS_COMENTARIOS

    with open(lista_exclusion, 'r', encoding='utf-8') as f:
        lista_de_exclusion = json.load(f)
        lista_de_exclusion = [_limpiar_texto(usuario) for usuario in lista_de_exclusion]

    NUEVOS_COMENTARIOS = _reemplazar_usuarios(comentarios, lista_de_exclusion)
    NUEVOS_COMENTARIOS = _trim_and_filter_comments(NUEVOS_COMENTARIOS)

    FILE = f'{archivo} reformateado.json'

    # Guardamos los resultados en un archivo JSON
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(NUEVOS_COMENTARIOS, f, ensure_ascii=False, indent=4)

    return FILE

if __name__ == '__main__':
    ARCHIVO = "Ncwi1DGAGkk comentarios.json"
    LISTA_DE_EXCLUSION_ARCHIVO = "Ncwi1DGAGkk usuarios.json"
    NUEVOS_COMENTARIOS = limpiar_texto(ARCHIVO, LISTA_DE_EXCLUSION_ARCHIVO)
    print(f"Texto limpio guardado en: {ARCHIVO} reformateado.json")
    print(f"Total de comentarios: {len(NUEVOS_COMENTARIOS)}")