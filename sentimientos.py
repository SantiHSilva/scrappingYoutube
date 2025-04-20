from textblob import TextBlob
import json

def obtener_texto_from_txt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

TEXTO = obtener_texto_from_txt('1744989070 comentarios.json reformateado.json')

def polaridad_por_palabra(texto):
    """
    Calcula la polaridad de cada palabra en el texto.
    
    Args:
        texto (str): Texto a analizar.
    
    Returns:
        dict: Diccionario con palabras y sus polaridades.
    """
    PALABRAS = texto
    polaridades = {}
    resumen = {
        'positivo': 0,
        'negativo': 0,
        'neutral': 0
    }

    comentario = 1

    for palabra in PALABRAS:
        blob = TextBlob(palabra)
        polaridad = blob.sentiment.polarity
        
        score = ""

        if polaridad > 0:
            score = "positivo"
        elif polaridad < 0:
            score = "negativo"
        else:
            score = "neutral"

        polaridades[f'comentario: #{comentario}'] = f'{score} - {polaridad}'
        resumen[score] += 1
        comentario += 1

    print('Polaridades:', polaridades)
    print('Resumen:', resumen)

    return polaridades

sentiment_score = polaridad_por_palabra(TEXTO)