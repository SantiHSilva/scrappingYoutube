from translate import Translator
from pyalex import Works
import re
from pyvis.network import Network
import requests
import random
import json

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
    """
    Formatea la palabra clave para que sea compatible con el API de PyAlex.
    """
    keyword = re.sub(r'[^a-zA-Z\s]', '', keyword)    
    keyword = keyword.strip()
    keyword = keyword.lower()
    keyword = keyword.replace(" ", "-")
    return keyword

def get_coincidenias(keyword):
    #https://api.openalex.org/autocomplete/keywords?q=university&mailto=team@ourresearch.or
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
        print(f'Obteniendo conceptos para la palabra clave: {palabra}')
        palabra = traducir_texto(palabra)
        print(f'Palabra clave traducida: {palabra}')
        palabra = formatKeyword(palabra)
        print(f'Palabra clave formateada: {palabra}')

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
    currentID = 0

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