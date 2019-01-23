#!/usr/bin/env python
""" 
Crear y publicar un archivo XML con el RSS para podcast que sea compatible con las plataformas más usadas 
Usa como parámetro único el directorio con los audios en MP3
"""

__author__ = "Andrés Vázquez"
__credits__ = ["Andrés Vázquez"]
__license__ = "GPL"
__version__ = "0.0.001"
__maintainer__ = "Andrés Vázquez"
__email__ = "andres@data99.com.ar"
__status__ = "Beta"

import sys
import os
from termcolor import colored
import json
from jinja2 import Template
from datetime import date, datetime
import urllib


# el primer parámetro de la llamada debe indicar la carpeta donde buscar
directorio = 'audios'
mp3s = []
# todos los links publicos en la web dependeran de una misma base dependiendo de donde se publique este código
base_web = 'https://avdata99.github.io/cadena-de-datos'
base_url = '{}/audios-y-rss'.format(base_web)

"""
dentro del "directorio" se espera que estén:
 - Los audios en formato MP3
 - Una imagen por cada audio con el mismo nombre de archivo que el MP3 pero con extensión PNG o JPG
 - Un archivo JSON con datos del episodio
 - Un archivo de información llamado info.json con datos del PODCAST en general
"""

# leer los datos del podcast
canal_info_file = '{}/info.json'.format(directorio)
canal_data_file = open(canal_info_file)
# guardar en un diccionario todo lo que dice el archivo info.json
canal_info = json.load(canal_data_file)

# fecha de ultima compilacion (ahora)
d = datetime.now()
canal_info['ultima_compilacion'] = d.strftime("%a, %d %b %Y %H:%M:%S +0300")

# buscar todos los archivos MP3s y guardarlos en una lista
for filename in sorted(os.listdir(directorio)):
    if filename.endswith('.mp3'):
        print('Archivo encontrado {}'.format(filename))
        mp3s.append(filename)

# para simplificar este proceso se espera que la imagen y la info estén en archivos con identico nombre pero diferente extensión
# imagen: jpg o png
# info del episodio: JSON

# guardar todo en un diccionario más elaborado
canal_info['episodios'] = [] # cada episodio se contruye revisando sus datos en diccionarios individuales

for mp3 in mp3s:

    # contruir el episodio de una propiedad a la vez
    # AUDIO del episodio -----------------------------
    url_mp3 = '{}/{}/{}'.format(base_url, directorio, mp3)
    episodio = {'url_audio': url_mp3}
    file_mp3 = '{}/{}'.format(directorio, mp3)
    episodio['audio_size_bytes'] = os.path.getsize(file_mp3)

    # IMAGEN del episodio -----------------------------
    base_name = mp3.replace('.mp3', '')
    episodio['base_name'] = base_name

    # preparar URL completa y encodeada para compartir
    episodio['full_url'] = '{}/{}.html'.format(base_web, base_name)
    episodio['full_url_encoded'] = urllib.parse.quote(episodio['full_url'])

    extensiones_imagenes_aceptadas = ['png', 'jpg']
    imagen_encontrada = None

    for ext in extensiones_imagenes_aceptadas:
        imagen = '{}/{}.{}'.format(directorio, base_name, ext)
        if os.path.isfile(imagen):
            imagen_encontrada = imagen
    
    if imagen_encontrada is None:
        print(colored('No se encontro la imagen de {}'.format(base_name), 'red'))
        sys.exit(1)
    else:
        print(colored('Se encontro la imagen de {}'.format(base_name), 'green'))

    url_imagen = '{}/{}'.format(base_url, imagen_encontrada)
    episodio['url_imagen'] = url_imagen

    # INFO del episodio -----------------------------
    datos_episodio = '{}/{}.json'.format(directorio, base_name)
    if not os.path.isfile(datos_episodio):
        print(colored('No se encontraron los datos del episodio {}'.format(base_name), 'red'))
        sys.exit(1)

    # abrir el archivo JSON, tomar todas sus propiedades y sumarlas (update) a este diccionario
    data_file = open(datos_episodio)
    episodio.update(json.load(data_file))

    # https://github.com/simplepie/simplepie-ng/wiki/Spec:-iTunes-Podcast-RSS#pubdate
    d = datetime(episodio["anio_publicacion"], episodio["mes_publicacion"], episodio["dia_publicacion"], 
                        episodio["hora_publicacion"], episodio["minuto_publicacion"])

    episodio['fecha_publicacion'] = d.strftime("%a, %d %b %Y %H:%M:%S +0300")

    episodio['titulo_encoded'] = urllib.parse.quote(episodio['titulo'])

    print('-------------------------------------')
    nice_json = json.dumps(episodio, indent=4)
    print('EPISODIO LISTO {}'.format(nice_json))
    print('-------------------------------------')    

    episodio['link'] = '{}/{}.html'.format(base_url, base_name) # se crea despues
    episodio['guid'] = episodio['link']
    canal_info['episodios'].append(episodio)
    canal_info['ultimo_episodio'] = episodio


# ya tengo todas las variables de contexto para aplicar al template (rss y html)

# aplicarla a todos los templates disponibles en la carpeta templates-rss
canal_info['RSSs'] = []  # dejar disponible para mostrar
for filename in os.listdir('templates-rss'):
    if filename.endswith('.tpl'):
        print('Template encontrado {}'.format(filename))
        base_template = filename.replace('.tpl', '')
        tpl = open('templates-rss/{}'.format(filename))
        template = Template(tpl.read())
        tpl.close()
        rss = template.render(canal_info)

        # escribir los resultados en un archivo llamado podcast.xml
        file_resultado = open('{}/podcast_{}'.format(directorio, base_template), 'w')
        file_resultado.write(rss)
        file_resultado.close()

        url_rss = '{}/{}/podcast_{}'.format(base_url, directorio, base_template)
        print(colored('Se genero RSS para {}. Una vez subido el feed a compartir estará en el link {}'.format(base_template, url_rss), 'green'))

        single_name = base_template.replace('.xml', '')
        canal_info['RSSs'].append({'nombre': single_name, 'url': url_rss})


# aplicarla a todos los templates disponibles en la carpeta templates-html

# crear la home del sitio
tpl = open('templates-html/home.html')
template = Template(tpl.read())
tpl.close()
index = template.render(canal_info)
file_resultado = open('../index.html', 'w')
file_resultado.write(index)
file_resultado.close()

# generar todos los HTMLs individuales
episodios = canal_info['episodios']
dic = {'canal': canal_info, 'episodios': episodios}

for episodio in episodios:
    # crear html del episodio
    tpl = open('templates-html/episode.html')
    template = Template(tpl.read())
    tpl.close()
    dic['episodio'] = episodio
    epihtml = template.render(dic)
    file_resultado = open('../{}.html'.format(episodio['base_name']), 'w')
    file_resultado.write(epihtml)
    file_resultado.close()