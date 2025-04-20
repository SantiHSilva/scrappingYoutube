from translate import Translator
from pyalex import Works
from pyvis.network import Network

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
    keyword = keyword.strip()
    keyword = keyword.lower()
    keyword = keyword.replace(" ", "-")
    return keyword

def graficar_conceptos(keyword, filename):
    palabra = keyword
    print(f'Obteniendo conceptos para la palabra clave: {palabra}')
    palabra = traducir_texto(palabra)
    print(f'Palabra clave traducida: {palabra}')
    palabra = formatKeyword(palabra)
    print(f'Palabra clave formateada: {palabra}')

    RESPONSE = Works().filter(
        keywords={"id": palabra}
    ).get()

    print(f'Conceptos encontrados: {len(RESPONSE)}')

    CONCEPTOS = []
    currentID = 0

    for work in RESPONSE:
        for concepto in work['concepts']:
            currentID += 1
            CONCEPTOS.append({
                'id': currentID,
                'display_name': concepto['display_name'],
                'level': concepto['level'],
                'score': concepto['score'],
            })

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
        )

    net.show(f"{filename} conceptos sin relacionar.html")

    for edge in EDGES:
        net.add_edge(
            edge['from'],
            edge['to'],
        )

    net.show(f"{filename} conceptos relacionado.html")
    print(f"{len(CONCEPTOS)} Conceptos guardados en: conceptos.html")

if __name__ == "__main__":
    graficar_conceptos("Machine Learning", "conceptos")