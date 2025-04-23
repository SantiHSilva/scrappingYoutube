import pandas as pd
import json
import matplotlib.pyplot as plt

def _obtener_texto_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def obtener_palabras_repetidas(filename, min_length=10):
    print(f'Buscando palabras repetidas en: {filename}, con longitud mínima de {min_length} caracteres.')

    TEXTO = _obtener_texto_from_json(filename)
    TEXTO = ' '.join(TEXTO)

    lista_texto = TEXTO.split(" ")

    palabras = []

    for palabra in lista_texto:
        if (len(palabra)>=min_length):
            palabras.append(palabra)
                
        word_count={}

        for palabra in palabras:
            if palabra in word_count.keys():
                word_count[palabra][0]+=1
            else:
                word_count[palabra]=[1]

    df = pd.DataFrame.from_dict(word_count).transpose()
    df.columns=["freq"]
    df.sort_values(["freq"], ascending=False, inplace=True)

    # Guardamos el DataFrame en un archivo CSV
    df.to_csv(f'{filename} palabras_repetidas.csv', index=True, header=True)

    print(f"Palabras repetidas guardadas en: {filename} palabras_repetidas.csv")
    print(f"Total de palabras: {len(df)}")

    # Obtener las 10 palabras más repetidas
    top_10 = df.head(10)
    
    # Crear la gráfica
    plt.figure(figsize=(12, 8))
    bars = plt.barh(top_10.index, top_10['freq'], color='skyblue')
    plt.gca().invert_yaxis()  # Para mostrar la mayor frecuencia arriba
    plt.title(f'Top 10 palabras más repetidas en {filename}', pad=20)
    plt.xlabel('Frecuencia')
    plt.ylabel('Palabras')
    
    # Añadir los valores en las barras
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                 f'{int(width)}', 
                 ha='left', va='center')
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Guardar la gráfica
    plot_filename = f'{filename} palabras_repetidas.png'
    plt.savefig(plot_filename)
    print(f"Gráfica guardada como: {plot_filename}")
    plt.close()
    
    return df

if __name__ == '__main__':
    filename = 'Ncwi1DGAGkk comentarios.json reformateado.json'
    min_length = 10
    df = obtener_palabras_repetidas(filename, min_length)
    # obtener las primeras 10 palabras más repetidas
    lista_de_palabras = df.head(10).index.tolist()
    print(f'La palabra más repetida es: {lista_de_palabras}')
