import pandas as pd
import json

def obtener_texto_from_txt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

TEXTO = obtener_texto_from_txt('1744989070 comentarios.json reformateado.json')
TEXTO = ' '.join(TEXTO)

lista_texto = TEXTO.split(" ")

palabras = []

for palabra in lista_texto:
  if (len(palabra)>=10): # Filtramos palabras de 6 o más letras
    palabras.append(palabra)
        
#Generamos un diccionario para contabilizar las palabras:

word_count={}

for palabra in palabras:
    if palabra in word_count.keys():
        word_count[palabra][0]+=1
    else:
        word_count[palabra]=[1]

# print(word_count)

df = pd.DataFrame.from_dict(word_count).transpose()
df.columns=["freq"]
df.sort_values(["freq"], ascending=False, inplace=True)
print(df.head(10))