# Transcripcion completa de cada episodio con Whisper.
# Genera <slug>.srt (con tiempos, es la fuente) y <slug>.txt (texto en parrafos, armado desde el .srt).
#
#   python transcribir-whisper.py <dir_audios> <dir_temporal> <dir_salida>
#   python transcribir-whisper.py <dir_audios> <dir_temporal> <dir_salida> --solo-txt   # rehace los .txt desde los .srt
import os, sys, re, glob, json, subprocess, wave, datetime
from collections import Counter

MODELO = 'large-v3-turbo'
ENCABEZADO = '''{titulo}

Transcripto con Whisper, sin corrección humana. Puede tener errores, sobre todo en nombres propios.
- Herramienta: faster-whisper {version} (https://github.com/SYSTRAN/faster-whisper)
- Modelo: {modelo}, int8_float16, GPU
- Parámetros: idioma es, filtro VAD, condition_on_previous_text=False
- Audio: {slug}.mp3
- Fecha: {fecha}

---

'''


def ts(s):
    ms = int(round(s * 1000))
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def leer_srt(path):
    bloques = open(path).read().strip().split('\n\n')
    return [' '.join(b.split('\n')[2:]).strip() for b in bloques if b.count('\n') >= 2]


def armar_parrafos(textos):
    """Une los fragmentos de Whisper en oraciones y parrafos legibles."""
    palabras = Counter(w for t in textos for w in re.findall(r'\w+', t))
    partes = []
    for t in textos:
        if not t:
            continue
        # sin contexto previo Whisper arranca cada fragmento con mayuscula: si el anterior no cerro
        # la oracion y la palabra se usa mas en minuscula en el resto del texto, va en minuscula
        if partes and not re.search(r'[.?!]["\')]*$', partes[-1]):
            m = re.match(r'(\w+)', t)
            if m and m.group(1)[0].isupper():
                w = m.group(1)
                if palabras[w.lower()] > palabras[w]:
                    t = w.lower() + t[len(w):]
        partes.append(t)

    # parrafo nuevo despues de una pregunta (suele ser cambio de quien habla)
    # o cuando el parrafo ya es largo y termina una oracion
    parrafos, actual, n = [], [], 0
    for t in partes:
        actual.append(t)
        n += len(t.split())
        cierra = re.search(r'[.?!]["\')]*$', t)
        if (t.rstrip().endswith('?') and n > 15) or (cierra and n > 140):
            parrafos.append(' '.join(actual))
            actual, n = [], 0
    if actual:
        parrafos.append(' '.join(actual))
    return [p[0].upper() + p[1:] for p in parrafos]


def escribir_txt(audios, out, slug, version, fecha):
    titulo = json.load(open(os.path.join(audios, slug + '.json')))['titulo']
    srt = os.path.join(out, slug + '.srt')
    txt = os.path.join(out, slug + '.txt')
    with open(txt + '.part', 'w') as f:
        f.write(ENCABEZADO.format(titulo=titulo, version=version, modelo=MODELO, slug=slug, fecha=fecha))
        f.write('\n\n'.join(armar_parrafos(leer_srt(srt))) + '\n')
    os.replace(txt + '.part', txt)


def main():
    audios, tmp, out = sys.argv[1:4]
    solo_txt = '--solo-txt' in sys.argv
    os.makedirs(out, exist_ok=True)
    import faster_whisper
    version = faster_whisper.__version__

    if solo_txt:
        for srt in sorted(glob.glob(os.path.join(out, '*.srt'))):
            slug = os.path.basename(srt)[:-4]
            fecha = datetime.date.fromtimestamp(os.path.getmtime(srt)).isoformat()
            escribir_txt(audios, out, slug, version, fecha)
            print('txt', slug, flush=True)
        return

    import numpy as np
    model = faster_whisper.WhisperModel(MODELO, device='cuda', compute_type='int8_float16')
    for mp3 in sorted(glob.glob(os.path.join(audios, '*.mp3'))):
        slug = os.path.basename(mp3)[:-4]
        srt = os.path.join(out, slug + '.srt')
        if os.path.exists(srt) and os.path.exists(os.path.join(out, slug + '.txt')):
            continue
        wav = os.path.join(tmp, slug + '-full.wav')
        subprocess.run(['ffmpeg', '-v', 'quiet', '-y', '-i', mp3, '-ac', '1', '-ar', '16000', wav], check=True)
        with wave.open(wav) as w:
            pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        segs = list(model.transcribe(pcm, language='es', vad_filter=True, condition_on_previous_text=False,
                                     initial_prompt='Cadena de datos, podcast de Andrés Vázquez sobre datos abiertos.')[0])
        os.remove(wav)
        with open(srt + '.part', 'w') as f:
            for i, s in enumerate(segs, 1):
                f.write('{}\n{} --> {}\n{}\n\n'.format(i, ts(s.start), ts(s.end), s.text.strip()))
        os.replace(srt + '.part', srt)
        escribir_txt(audios, out, slug, version, datetime.date.today().isoformat())
        print('ok', slug, len(segs), flush=True)


if __name__ == '__main__':
    main()
