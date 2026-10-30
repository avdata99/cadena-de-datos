# Transcripciones

Transcripción automática de cada episodio, hecha con Whisper sobre el MP3 original. **No están corregidas a mano**: pueden tener nombres propios mal escritos y errores de reconocimiento.

Por cada episodio hay dos archivos, con el mismo nombre que el audio en `audios-y-rss/audios/`:

- `<episodio>.txt`: texto corrido en párrafos. Al principio lleva el título y los datos de cómo se transcribió.
- `<episodio>.srt`: subtítulos con tiempos, se pueden subir a YouTube.

## Cómo se generaron

- Herramienta: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (software libre, MIT)
- Modelo: `large-v3-turbo`, cuantizado `int8_float16`, en GPU local
- Parámetros: idioma `es`, filtro VAD, `condition_on_previous_text=False`
- Script: [`extras/transcribir-whisper.py`](../extras/transcribir-whisper.py)

```bash
pip install faster-whisper nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
# las librerias CUDA instaladas por pip tienen que estar en LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$(python -c "import nvidia.cublas.lib as a, nvidia.cudnn.lib as b; print(list(a.__path__)[0] + ':' + list(b.__path__)[0])")
python extras/transcribir-whisper.py audios-y-rss/audios /tmp transcripciones
```

El script saltea los episodios que ya tienen `.txt` y `.srt`, así que se puede cortar y retomar.

El `.srt` es la fuente: el `.txt` se arma desde él (une fragmentos, corrige mayúsculas y corta párrafos después de cada pregunta). Para rehacer los `.txt` sin volver a transcribir:

```bash
python extras/transcribir-whisper.py audios-y-rss/audios /tmp transcripciones --solo-txt
```
