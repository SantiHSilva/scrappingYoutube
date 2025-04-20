import pandas as pd
import json

def _obtener_texto_from_txt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def obtener_palabras_repetidas(filename, min_length=10):
    print(f'Buscando palabras repetidas en: {filename}, con longitud mínima de {min_length} caracteres.')

    TEXTO = _obtener_texto_from_txt(filename)
    TEXTO = ' '.join(TEXTO)

    lista_texto = TEXTO.split(" ")

    palabras = []

    for palabra in lista_texto:
        if (len(palabra)>=min_length): # Filtramos palabras de 6 o más letras
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

    return df

if __name__ == '__main__':
    filename = 'Ncwi1DGAGkk comentarios.json reformateado.json'
    min_length = 10
    df = obtener_palabras_repetidas(filename, min_length)
    # obtener las primeras 10 palabras más repetidas
    lista_de_palabras = df.head(10).index.tolist()
    print(f'La palabra más repetida es: {lista_de_palabras}')
