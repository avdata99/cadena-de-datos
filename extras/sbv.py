""" Procesar archivos SBV 
Los archivos SBV son generados por YouTube como transcripción automática de los textos.
La idea es poder pasarlos a texto reutilizables en otros contextos.
"""
import sys
import re

print("sbv.py file.sbv -> genera file.txt")
print("Pensado para entrevistas")

sbv_file = sys.argv[1]
base_name = sbv_file.replace('.sbv', '')

f = open(sbv_file, 'r')
sbv_txt = f.read()
f.close()

registros = []

for linea in sbv_txt.split('\n'):
    if re.match('[0-9]:[0-9]', linea):
        ts = linea.split(',')
        tiempo = {'ini': ts[0], 'fin': ts[1]}
        ultimo_registro = {'tiempo': tiempo, 'texto': ''} 
        registros.append(ultimo_registro)
    else:
        if linea.strip() != '':
            ultimo_registro['texto'] = linea

print('Registros: {}'.format(len(registros)))

# imprimir un srt
srt_file = '{}.srt'.format(base_name)
f = open(srt_file, 'w')
c = 1
for registro in registros:
    f.write('{}\n'.format(c))
    f.write('{} --> {}\n'.format(registro['tiempo']['ini'].replace('.', ','), registro['tiempo']['fin'].replace('.', ',')))
    f.write('{}\n'.format(registro['texto']))
    f.write('\n')
    c += 1
f.close()

# limpiar un poco para escribir un txt
txt_file = '{}.txt'.format(base_name)

textos = [linea['texto'] for linea in registros]
txt = ' '.join(textos)
txt = txt.replace('  ', ' ')
txt = txt.replace('.  ', '.\n')  # dos espacios como markdown



f = open(txt_file, 'w')
f.write(txt)
f.close()

print('FINAL ********************')
print(txt)