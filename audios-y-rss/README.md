# Pruebas para un RSS compatible con múltiples plataformas

Generación de feeds RSS. Usado como ejemplo de programación lineal y de estructuras básicas de datos en Python.  

## Pasos a seguir

En primer lugar se requiere crear un entorno con _Python 3_
```
python3 -m venv ~/genrss
# ingresar al entorno
source ~/genrss/bin/activate
```

E instalar las librerías requeridas
```
pip install -r requirements.txt
```

### Crear una carpeta para los audios
Para dar de alta un nuevo podcast se crea (dentro de la carpeta _audios) un nuevo directorio con el nombre.

### Subir la info general del podcast
Dentro de ese directorio crear un archivo _info.json_. Este tiene datos generales del podcast.  
Ejemplo (los campos podrían cambiar, revisar alguno ya funcionando en este repo).  

```
{
    "titulo": "Entrevistas y audios de Andrés Vázquez",
    "link": "https://andresvazquez.com.ar/",
    "descripcion": "Audio donde participé y guardo como archivo",
    "lenguaje": "es-ar",
    "ttl_minutos": "240",
    "autor": "Andrés Vázquez",
    "imagen_titulo": "Entrevistas Andrés Vázquez",
    "imagen_url": "https://andresvazquez.com.ar/blog/wp-content/uploads/2016/11/Selecci%C3%B3n_419-1024x512.png",
    "imagen_link": "https://andresvazquez.com.ar/",
    "webmaster_email": "andres@data99.com.ar",
    "editor_email": "andres@data99.com.ar"
}
```

### Colocar los audios
En esa carpeta colocar todos los archivos MP3 (por ahora único formato compatible).  
Con cada emisión se coloca un audio nuevo y se repiten los pasos que siguen.  

#### Desde RadioCut
Si querés bajar tus **recortes de RadioCut** para subir a alguna plataforma y generar tu propio RSS acá tenes una opción:
https://github.com/mgaitan/radiocut_downloader.  

Ejemplo para descargar un recorte (se hace desde nuestro nuevo directorio así el archivo final queda allí):

```
radiocut https://radiocut.fm/audiocut/eugenia-monte-este-fallo-es-historico-para-el-feminismo/
```

### Subir una imagen
Por cada audio se requiere en la misma carpeta una imagen **con exactamente el mismo nombre** del audio pero extensión cambiada (_png_ o _jpg_).  

### Subir la info del episodio
Por cada audio se requiere en la misma carpeta un archivo de datos JSON **con exactamente el mismo nombre** del audio pero extensión cambiada a _json_.    

Ejemplo (los campos podrían cambiar, revisar alguno ya funcionando en este repo).  
```
{
    "titulo": "Charla en el Podcast de ILDA",
    "link": "https://andresvazquez.com.ar/blog/en-el-podcast-de-ilda-los-datos-cerca-del-vecino/",
    "guid": "https://andresvazquez.com.ar/blog/en-el-podcast-de-ilda-los-datos-cerca-del-vecino/",
    "fecha_publicacion": "Fri, 20 Jul 2018 15:55:23 +0300",
    "descripcion": "Entrevista en el podcast de la Iniciativa Latginoamericana de Datos Abiertos. Con Silvana Fumega y JuanI Belbis."
}
```

### Procesar los datos  y generar el RSS final
Con el comando _generate-rss_ se puede procesar (por primera vez o como actualizacion al agregar un audio) un podcast (carpeta)

Ejemplo (usar con el nombre de la carpeta requerida)
```
python generate-rss.py audios/entrevistas-andres
```

Este comando informará si hay errores y si no fuera así mostraría los links finales de los feeds para cada plataforma.  
Ejemplo:

```
Template encontrado googleplay.xml.tpl
Se genero RSS para googleplay.xml. Una vez subido el feed a compartir estará en el link https://avdata99.github.io/test-rss-to-all-platforms/audios/entrevistas-andres/podcast_googleplay.xml

Template encontrado atom.xml.tpl
Se genero RSS para atom.xml. Una vez subido el feed a compartir estará en el link https://avdata99.github.io/test-rss-to-all-platforms/audios/entrevistas-andres/podcast_atom.xml

Template encontrado itunes.xml.tpl
Se genero RSS para itunes.xml. Una vez subido el feed a compartir estará en el link https://avdata99.github.io/test-rss-to-all-platforms/audios/entrevistas-andres/podcast_itunes.xml
```

## Templates
Los feeds RSS generados dependen del destinatario. Hay especificaciones para Itunes, Google y otros. La idea es hacer variados feeds compatibles con todas las necesidades.  
La carpeta _templates_ tienen un archivo (template Jinja2) por cada formato de salida.  
El comando _generate-rss_ creará una archivo por cada template existente.  

Para entender el estandar XML/RSS extraje info de:
 - [GeekNewsCentral](https://geeknewscentral.com/podcast.xml)
 - [Shouldertheboulder](http://shouldertheboulder.com/article/generate-your-itunespodcast-rss-feed-with-rock)
 - [SysAdministrivia](https://sysadministrivia.com/news/howto-podcast)


