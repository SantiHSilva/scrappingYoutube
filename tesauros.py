from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk import download
import json

# Descargar recursos de NLTK
download('stopwords')
download('punkt_tab')

def obtener_texto_from_txt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file) 

# Palabras clave
tesauros = [
    {
        "nombre": "Tecnología de la información",
        "keywords": [
            'acceso', 'aleatorio', 'administración', 'oficina', 'análisis', 'datos',
            'aplicación', 'telecomunicaciones', 'informática', 'atribución', 'frecuencias',
            'automatización', 'bibliotecas', 'codificación', 'comunicación', 'espacial',
            'móvil', 'configuración', 'multipuesta', 'correo', 'electrónico', 'digitalización',
            'diseño', 'ordenador', 'fabricación', 'asistida', 'formato', 'datos',
            'infografia', 'informatización', 'archivos', 'ingeniería', 'televisión',
            'telefónica', 'inteligencia', 'artificial', 'intercambio', 'datos',
            'lenguaje', 'programación', 'lingüística', 'informática', 'ofimática',
            'organización', 'ficheros', 'procesamiento', 'programa', 'ordenador',
            'programación', 'informática', 'radiodifusión', 'satélite', 'radioingeniería',
            'reconocimiento', 'caracteres', 'formas', 'recopilación', 'datos',
            'red', 'telecomunicaciones', 'reprografia', 'robótica', 'servicio',
						'oficina', 'sistema', 'línea', 'experto', 'software', 'código', 'abierto',
						'tecnología', 'comunicación', 'información', 'radiodifusión', 'telecomunicación',
						'teleconferencia', 'teledetección', 'telemática', 'televisión', 'alta',
						'definición', 'circuito', 'cerrado', 'color', 'cable', 'traducción',
						'automática', 'transmisión', 'internacional', 'tratamiento', 'textos',
						'vídeojuego'
				]
		},
	{
				"nombre": "Diseño de sistemas",
				"keywords": [
						'análisis', 'redes', 'cibernética', 'investigación', 'interdisciplinaria',
						'optimización', 'programa', 'ordenador', 'técnica', 'administrativa',
						'toma', 'decisiones', 'algoritmo', 'lógica', 'matematica', 'algebra', 'análisis',
				]
		},
		{
				"nombre": "Investigación y desarrollo",
				"keywords": [
						'ingeniería', 'innovación', 'científica', 'investigación', 'operativa',
						'programa', 'investigación', 'horario', 'escolar', 'asistencia', 'escolar',
				]
		},
		{
				"nombre": "Horario Escolar",
				"keywords": [
						'asistencia', 'escolar', 'permiso', 'estudios', 'tiempo', 'vacaciones',
						'agrupamiento', 'educacional', 'aptitudes', 'alojamiento', 'año',
						'beca', 'investigación', 'viaje', 'bienestar', 'comedor',
						'condiciones', 'admisión','educación','inclusiva','empleo','fin',
						'escuela','gestión','horario','orientación','pedagógica','profesional',
						'préstamo','servicio','salud','transporte', 'subvención', 'educativa', 'vacaciones', 'escolares'
				]
		},
		{
				"nombre": "Gestión educacional",
				"keywords": [
						'administración', 'educación', 'agrupamiento', 'educacional', 'articulación',
						'educativa', 'asistencia', 'escolar', 'autonomía', 'educativa',
						'condiciones', 'empleo', 'docente', 'descentralización', 'financiación',
						'integración', 'programas', 'intercambio'
				]
		},
		{
				"nombre": "Algoritmo",
				"keywords": [
						'lógica', 'matematica', 'algebra', 'análisis', 'regresión', 'variancia',
						'estadística', 'factorial', 'funcional', 'matemático', 'multivariado',
						'numerico', 'aritmética', 'cálculo', 'correlación', 'datos',
						'estadísticos', 'ecuación', 'inferencial', 'interpolación',
						'combinatoria', 'matemáticas', 'estadísticas', 'modelo', 'matemático',
						'presentación', 'estadísticas'
				]
		},
		{
				"nombre": "Usuario de información",
				"keywords": [
						'estudio', 'usuarios', 'información', 'formación', 'necesidad',
						'usuario', 'bibliotecas', 'comunicación', 'sociedad', 'información', 'usuario',
				]
		},
		{
				"nombre": "Enseñanza superior",
				"keywords": [
						'nivel', 'enseñanza', 'educación', 'primera', 'infancia', 'secundaria',
						'curso', 'postuniversitario', 'universitario', 'adultos', 'científica',
						'profesional', 'estudiante', 'instituto', 'plan', 'servicio'
				]
		},
		{
				"nombre": "Toma de decisiones",
				"keywords": [
						'operación', 'administrativa', 'cibernética', 'diseño', 'sistemas',
						'evaluación', 'juicio', 'valor', 'previsión', 'racionalización',
						'razonamiento', 'resolución', 'problemas', 'teoría', 'decisión'
				]
		},
		{
				"nombre": "Tendencia educacional",
				"keywords": [
						'evolución', 'efectivos', 'innovación', 'educacional', 'prospección'
				]
		}
]

# keyword_counts = Counter([word for word in filtered_tokens if word in keywords])

def contar_palabras_clave(tesauros, tokens):
	conteos = {}
	for tesauro in tesauros:
		conteos[tesauro["nombre"]] = Counter([word for word in tokens if word in tesauro["keywords"]])
	return conteos

def mostrar_conteos(conteos):
	for nombre, conteo in conteos.items():
		print(f"\n{nombre}:")
		for palabra, cantidad in conteo.most_common(10):
			print(f"{palabra}: {cantidad}")

def guardar_conteos(conteos, filename):
	with open(f'{filename} conteos.json', 'w', encoding='utf-8') as f:
		json.dump(conteos, f, ensure_ascii=False, indent=4)

def obtener_tesauros(filename):
	TEXTO = obtener_texto_from_txt(filename)
	TEXTO = ' '.join(TEXTO)

	stop_words = set(stopwords.words('spanish'))
	tokens = word_tokenize(TEXTO.lower())
	filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
	conteos = contar_palabras_clave(tesauros, filtered_tokens)
	mostrar_conteos(conteos)
	guardar_conteos(conteos, filename)

if __name__ == "__main__":
	obtener_tesauros('Ncwi1DGAGkk comentarios.json reformateado.json')
