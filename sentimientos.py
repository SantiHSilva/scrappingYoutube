from textblob import TextBlob
import json

def obtener_texto_from_txt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def polaridad_por_palabra(filename):
    texto = obtener_texto_from_txt(filename)

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

    print(f"Resumen de polaridades: {resumen}")
    print(f"Total de palabras: {len(PALABRAS)}")

    # Guardamos el resumen en un archivo JSON
    with open(f'{filename} polaridades resumido.json', 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, indent=4)

    # Guardamos las polaridades en un archivo JSON
    with open(f'{filename} polaridades detallado.json', 'w', encoding='utf-8') as f:
        json.dump(polaridades, f, ensure_ascii=False, indent=4)

    return polaridades

if __name__ == '__main__':
    FILENAME = 'Ncwi1DGAGkk comentarios.json reformateado.json'
    polaridad_por_palabra(FILENAME)