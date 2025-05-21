from textblob import TextBlob # Sirve para analizar el texto y obtener la polaridad
import json # Para manejar archivos JSON
import matplotlib.pyplot as plt # Para graficar los resultados

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
    comentario = 1 # Para el registro de comentarios
    for palabra in PALABRAS:
        blob = TextBlob(palabra)
        polaridad = blob.sentiment.polarity
        
        score = ""
        # Clasificamos la polaridad
        if polaridad > 0:
            score = "positivo"
        elif polaridad < 0:
            score = "negativo"
        else:
            score = "neutral"

        # Guardamos la polaridad en el diccionario
        polaridades[f'comentario: #{comentario}'] = f'{score} - {polaridad}'
        resumen[score] += 1 # Actualizamos el resumen
        comentario += 1 # Incrementamos el contador de comentarios

    print(f"Resumen de polaridades: {resumen}")
    print(f"Total de palabras: {len(PALABRAS)}")

    # Guardamos el resumen en un archivo JSON
    with open(f'{filename} polaridades resumido.json', 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, indent=4)

    # Guardamos las polaridades en un archivo JSON
    with open(f'{filename} polaridades detallado.json', 'w', encoding='utf-8') as f:
        json.dump(polaridades, f, ensure_ascii=False, indent=4)
    
    # Generar y guardar la gráfica
    generar_grafica_polaridad(resumen, filename)
    
    return polaridades

def generar_grafica_polaridad(resumen, filename):
    """
    Genera y guarda una gráfica de barras con el resumen de polaridades.
    
    Args:
        resumen (dict): Diccionario con el resumen de polaridades.
        filename (str): Nombre del archivo original para nombrar la gráfica.
    """
    categorias = list(resumen.keys())
    valores = list(resumen.values())
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categorias, valores, color=['green', 'red', 'gray'])
    
    # Añadir etiquetas con los valores
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}', ha='center', va='bottom')
    
    plt.title('Resumen de Polaridad de Comentarios')
    plt.xlabel('Categoría de Polaridad')
    plt.ylabel('Cantidad de Comentarios')
    
    # Guardar la gráfica
    nombre_grafica = f"{filename} polaridad.png"
    plt.savefig(nombre_grafica)
    print(f"Gráfica guardada como: {nombre_grafica}")
    plt.close()

if __name__ == '__main__':
    FILENAME = './Ncwi1DGAGkk/Ncwi1DGAGkk comentarios.json reformateado.json'
    polaridad_por_palabra(FILENAME)