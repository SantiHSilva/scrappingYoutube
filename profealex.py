from translate import Translator # Traducir palabras claves
from pyalex import Works # API de OpenAlex para la obtención de articulos
import re # Libreria para expresiones regulares, para limpiar las palabras claves
from pyvis.network import Network # Libreria para graficar los conceptos
import requests # Libreria para hacer peticiones HTTP
import random # Libreria para generar colores aleatorios
import json # Libreria para guardar los conceptos en un archivo JSON

TRADUCTOR = Translator(from_lang='es', to_lang='en')

def traducir_texto(texto):
    """
    Traduce el texto de español a inglés.
    """
    try:
        traduccion = TRADUCTOR.translate(texto)
        return traduccion
    except Exception as e:
        print(f'Error al traducir el texto: {e}')
        return texto
    
# keywords debe estar en inglés y cada espacio es un "-"

def formatKeyword(keyword):
    # Removemos caracteres que no sean letras
    keyword = re.sub(r'[^a-zA-Z\s]', '', keyword)
    # Removemos espacios en blanco al principio y al final
    keyword = keyword.strip()
    # Removemos espacios en blanco entre palabras
    keyword = keyword.lower()
    # Reemplazamos espacios en blanco por guiones
    keyword = keyword.replace(" ", "-")
    return keyword

def get_coincidenias(keyword):
    try:
        respuesta = requests.get('https://api.openalex.org/autocomplete/keywords',
                                {
                                    "q": keyword,
                                    "mailto": "team@ourresearch.or"
                                })
        respuesta.raise_for_status()
        coincidencias = respuesta.json()['results']
        return coincidencias
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener coincidencias: {e}')
        return []    

def graficar_conceptos(keywords = [], filename = ""):

    RESPONSES = []
    PALABRA_ELEGIDA = None

    for keyword in keywords:

        if(len(RESPONSES) > 0):
            print('Ya se han encontrado conceptos, no se continuara buscando coincidencias')
            break

        palabra = keyword
        palabra = traducir_texto(palabra)
        palabra = formatKeyword(palabra)

        if not palabra:
            print('No se pudo traducir la palabra clave')
            continue

        coincidencias = get_coincidenias(palabra)

        for coincidencia in coincidencias:
            print(f'Coincidencia: {coincidencia["display_name"]}')
            palabra = coincidencia['display_name']
            palabra = formatKeyword(palabra)
            print(f'Palabra clave formateada: {palabra}')

            RESPONSE = Works().filter(
                keywords={"id": palabra}
            ).get()

            print(f'Conceptos encontrados: {len(RESPONSE)}')

            if(len(RESPONSE) > 0):
                RESPONSES.append(RESPONSE)
                PALABRA_ELEGIDA = palabra
                break

    CONCEPTOS = []

    def colores_por_nivel(CONCEPTOS):
        COLORES_POR_NIVEL = []
        for concepto in CONCEPTOS:
            if concepto['level'] not in [c['level'] for c in COLORES_POR_NIVEL]:
                color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                COLORES_POR_NIVEL.append({
                    'level': concepto['level'],
                    'color': color,
                })

        return COLORES_POR_NIVEL
    
    currentID = 0
    for works in RESPONSES:
        for work in works:
            for concepto in work['concepts']:
                currentID += 1
                CONCEPTOS.append({
                    'id': currentID,
                    'display_name': concepto['display_name'],
                    'level': concepto['level'],
                    'score': concepto['score'],
                })

    COLORES = colores_por_nivel(CONCEPTOS)

    # si el display_name esta repetido, sumar el score
    NEW_CONCEPTOS = []

    for concepto in CONCEPTOS:
        if concepto['display_name'] not in [c['display_name'] for c in NEW_CONCEPTOS]:
            NEW_CONCEPTOS.append(concepto)
        else:
            for c in NEW_CONCEPTOS:
                if c['display_name'] == concepto['display_name']:
                    c['score'] += concepto['score']

    CONCEPTOS = NEW_CONCEPTOS

    EDGES = []
    # relacionar IDS si corresponden al mismo level
    # iterar 2 veces
    for concepto1 in CONCEPTOS:
        for concepto2 in CONCEPTOS:
            if concepto1['level'] == concepto2['level'] and concepto1['id'] != concepto2['id']:
                EDGES.append({
                    'from': concepto1['id'],
                    'to': concepto2['id'],
                })

    net = Network(
        height="100vh",
        width="100vh",
        directed=True,
        notebook=True,
    )

    for concepto in CONCEPTOS:
        net.add_node(
            concepto['id'],
            label=concepto['display_name'],
            value=concepto['score'],
            color=next((color['color'] for color in COLORES if color['level'] == concepto['level']), '#97c2fc'),
        )

    print(f"Guardando {len(CONCEPTOS)} Conceptos en: conceptos.html")

    net.show(f"{filename} conceptos {PALABRA_ELEGIDA} sin relacionar.html")

    print(f'Guardando {len(EDGES)} Relaciones en: conceptos relacionado.html')

    for edge in EDGES:
        net.add_edge(
            edge['from'],
            edge['to'],
        )

    net.show(f"{filename} conceptos {PALABRA_ELEGIDA} relacionado.html")

    with open(f"{filename} conceptos {PALABRA_ELEGIDA} logs.json", "w") as f:
        json.dump(CONCEPTOS, f, indent=2)

    return PALABRA_ELEGIDA

if __name__ == "__main__":
    graficar_conceptos(['Tourism'], "conceptos")