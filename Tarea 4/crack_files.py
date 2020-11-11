import os
import time

# HASHCAT = '~/hashcat-6.1.1/hashcat'
HASHCAT = 'hashcat'

FILES_PATH = './ArchivoTarea4'

DICCIONARIO_1 = FILES_PATH + '/diccionarios/diccionario_1.dict'
DICCIONARIO_2 = FILES_PATH + '/diccionarios/diccionario_2.dict'

ARCHIVO_1 = {'path': FILES_PATH + '/Hashes/archivo_1',
             'mode': 0, 'output': FILES_PATH + '/cracked/archivo_1.txt'}
ARCHIVO_2 = {'path': FILES_PATH + '/Hashes/archivo_2',
             'mode': 0, 'output': FILES_PATH + '/cracked/archivo_2.txt'}
ARCHIVO_3 = {'path': FILES_PATH + '/Hashes/archivo_3',
             'mode': 0, 'output': FILES_PATH + '/cracked/archivo_3.txt'}
ARCHIVO_4 = {'path': FILES_PATH + '/Hashes/archivo_4',
             'mode': 0, 'output': FILES_PATH + '/cracked/archivo_4.txt'}
ARCHIVO_5 = {'path': FILES_PATH + '/Hashes/archivo_5',
             'mode': 0, 'output': FILES_PATH + '/cracked/archivo_5.txt'}

archivos = [ARCHIVO_1]
# os.system('ls ' + FILES_PATH)
# os.system(HASHCAT + ' -b')
# os.system('hashcat -b -D 1,2')

# Crackeo de los archivos
for archivo in archivos:
    start_time = time.time()
    os.system(HASHCAT + ' -m ' + str(archivo['mode']) + ' -o ' + archivo['output'] +
              ' ' + archivo['path'] + ' ' + DICCIONARIO_2)
    print("--- %s seconds ---" % (time.time() - start_time))

# ./hashcat - m 0 - o ../Google\ Drive/Material\ estudio/Criptografía/Tarea\ 4/ArchivoTarea4/Hashes/cracked11.txt ../Google\ Drive/Material\ estudio/Criptografía/Tarea\ 4/ArchivoTarea4/Hashes/archivo_11 ../Google\ Drive/Material\ estudio/Criptografía/Tarea\ 4/ArchivoTarea4/diccionarios/diccionario_1.dict
