import os
import time
import bcrypt
import socket
import sys
import tqdm

BCRYPT_PASSWORD = '@X1&u2#6Zjwsx&bl'
HASHCAT = 'hashcat'
FILES_PATH = './archivos'

DICCIONARIO_1 = FILES_PATH + '/diccionarios/diccionario_1.dict'
DICCIONARIO_2 = FILES_PATH + '/diccionarios/diccionario_2.dict'

FILE_1 = {'path': FILES_PATH + '/Hashes/archivo_1',
             'mode': 0, 'output': FILES_PATH + '/cracked/archivo_1.txt'}
FILE_2 = {'path': FILES_PATH + '/Hashes/archivo_2',
             'mode': 10, 'output': FILES_PATH + '/cracked/archivo_2.txt'}
FILE_3 = {'path': FILES_PATH + '/Hashes/archivo_3',
             'mode': 10, 'output': FILES_PATH + '/cracked/archivo_3.txt'}
FILE_4 = {'path': FILES_PATH + '/Hashes/archivo_4',
             'mode': 1000, 'output': FILES_PATH + '/cracked/archivo_4.txt'}
FILE_5 = {'path': FILES_PATH + '/Hashes/archivo_5',
             'mode': 1800, 'output': FILES_PATH + '/cracked/archivo_5.txt'}

# Funcion que se encarga de crackear los archivos

def crack_files(files):
    for file in files:
        command = "hashcat -m " + str(file['mode']) + ' -o ' + file['output'] + ' ' + file['path'] + ' ' + DICCIONARIO_2 + ' --force' 
        start_time = time.time()
        os.system(command)
        print("--- %s seconds ---" % (time.time() - start_time))

# Crea el archivo consolidado con todas las contrasenas
def create_file(files):
    new_file = open('passwords.txt', 'a')
    for file in files:
        password_file = open(file, 'r')
        for line in password_file:
            clean_password = line.split(':')[-1]
            new_file.write(clean_password)

# Funcion encargada de rehashear las contrasenas en bcrypt
def rehash():
    rehashed_passwords = open('passwords_bcrypt.txt', 'a')
    passwords = open('passwords.txt', 'r')
    print('Start rehash')
    start_time = time.time()
    for password in passwords:
        hashed = bcrypt.hashpw(password = password.strip().encode('utf-8'), salt = bcrypt.gensalt(rounds=10))
        rehashed_passwords.write(hashed.decode('utf-8') + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))

# Encripta utilizando la llave publica
def encrypt_passwords(public_key, n, passwords):
    rsa_passwords = open('rsa_passwords.txt', 'a')
    print('=== Encriptando ===')
    for password in passwords:
        # Convierte cada letra en la contrasena a numeros, basado en el caracter utilizando a^b mod(m)
        cipher_password = [pow(ord(char), int(public_key.decode('utf-8')), int(n.decode('utf-8'))) for char in password]
        cipher_password = ''.join(map(lambda x: str(x), cipher_password))
        rsa_passwords.write(cipher_password + '\n')
    print('=== Finalizo encriptado ===')

# Funcion encargada de recibir la llave publica
def recv_message(sock):
    try:
        header = sock.recv(2)
        while b':' not in header:
            header += sock.recv(2) # Recibe de 2 bytes a la vez 
        size_of_package, separator, message_fragment = header.partition(b':')
        message = sock.recv(int(size_of_package))
        full_message = message_fragment + message
        return full_message
    except OverflowError:
        return 'OverflowError'
    except:
        print('unexpected error')
        raise


# Envia el archivo al cliente
def send_file(sock):
    filename = 'rsa_passwords.txt'
    # Obtiene el tamano del archivo en bytes
    filesize = os.path.getsize(filename)
    print('=== Enviando archivo ===')
    # Envia el tamano y nombre del archivo
    sock.send(f'{filesize}:{filename}'.encode())
    progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, 'rb') as file:
        for _ in progress:
            # Lee los bytes desde el archivo
            bytes_read = file.read(4096)
            if not bytes_read:
                # Termina la transmision
                break
            # Envia los bytes
            sock.sendall(bytes_read)
            # Actualiza la barra de progreso
            progress.update(len(bytes_read))
    print('=== Finaliza envio de archivo ===')


FILES = [FILE_1, FILE_2,FILE_3,FILE_4,FILE_5]

crack_files(FILES)

create_file([FILE_1['output'], FILE_2['output'], FILE_3['output'], FILE_4['output'], FILE_5['output']])

rehash()

# Crea el TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta al servidor
server_address = ('localhost', 10009)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

BUFFER_SIZE = 1024

try:
    # Envia la peticion de llave publica
    message = b'REQUEST_PUBLIC_KEY'
    print('Sending {}'.format(message))
    sock.sendall(message)

    # Recibe la respuesta
    public_key = recv_message(sock)
    n = ''
    if public_key:
        public_key, separator, n = public_key.partition(b':')
    print('public_key {}'.format(public_key.decode('utf-8')))
    passwords_bcrypt = open('passwords_bcrypt.txt', 'r')
    encrypt_passwords(public_key, n, passwords_bcrypt)
    send_file(sock)

finally:
    print('closing socket')
    sock.close()