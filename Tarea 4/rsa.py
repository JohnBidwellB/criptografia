import random
import socket
import sys
import tqdm
import os
import numpy as np

PRIME_LIMIT = 1000000000

# chequea si un numero es primo
def is_prime(num):
	if num == 2:
		return True
	if num < 2 or num % 2 == 0:
		return False
	for n in range(3, int(num ** 0.5) + 2, 2):
		if num % n == 0:
			return False
	return True

# Retorna un numero primo
def get_prime(limit = PRIME_LIMIT):
	num = 0
	while True:
		num = random.randint(0,limit)
		if is_prime(num):
			break
	return num

# Calcula el maximo comun divisor entre dos numeros
def greatest_common_divisor(a, b):
	while b != 0:
		a, b = b, a % b
	return a

# Calcula el inverso multiplicativo modular
def modular_multiplicative_inverse(e, phi):
	if e == 0:
		return (phi, 0, 1)
	else:
		g, y, x = modular_multiplicative_inverse(phi % e, e)
	return (g, x - (phi // e) * y, y)

# Genera las llaves publicas y privadas
def generate_keys(p, q):
	if not (is_prime(p) and is_prime(q)):
		raise ValueError('Ambos numeros deben ser primos')
	elif p == q:
		raise ValueError('Ambos numeros deben ser distintos')

	# Computa n
	n = p * q

	# Computa phi
	phi = (p - 1) * (q - 1)

	# Calcula la llave de encriptacion
	e = random.randrange(1, phi) # Escoge un numero entero
	g = greatest_common_divisor(e, phi) # Calcula el maximo comun divisor
	while g != 1: # Calcula numero hasta encontrar coprimos
		e = random.randrange(1, phi) 
		g = greatest_common_divisor(e, phi) 

	# Calcula la llave de desencriptacion
	d = modular_multiplicative_inverse(e, phi)[1]
	d = d % phi
	if d < 0:
		d += phi

	# Llave publica (e), llave privada(d) y n
	return (e, d, n)

# Desencripta los hashes RSA
def decrypt(private_key, n, cipher_text):
	try: 
		password = [chr(pow(ord(char), private_key, n)) for char in cipher_text]
		return ''.join(password)
	except TypeError as e:
		pass

# Procesa el recibir el archivo con las contrasenas cifradas
def receive_file(connection):
	print('=== Recibiendo arvchivo ===')
	received = connection.recv(4096).decode()
	filesize, filename = received.split(':')
	# Elimina la path absoluta (siesque esta)
	filename = os.path.basename(filename)

	# Convierte el tamano del archivo a entero
	filesize = int(filesize)

	# Actualiza el nombre del archivo para diferenciarlo del archivo enviado por el cliente
	filename = 'server-' + filename

	# Comienza a recibir el archivo
	progress = tqdm.tqdm(range(filesize), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024 )
	with open(filename, 'wb') as file:
		for _ in progress:
			# Lee 1024 bytes desde el socket
			bytes_read = connection.recv(4096)
			if not bytes_read:
				# Nada es recibido
				break
			# Escribe al archivo los bytes recibidos
			file.write(bytes_read)
			# Actualiza la barra de progreso
			progress.update(len(bytes_read))
	print('=== Finaliza de recibir archivo ===')
	return filename

# Desencripta los hash de RSA a bcrypt
def decrypt_file(private_key, n, filename):
	print('=== Desencriptar archivo ===')
	file = open(filename, 'r')
	for rsa_password in file:
		bcrypt_password = decrypt(private_key, n, rsa_password)
	print('=== Finaliza desencriptado ===')

# Guarda los bcrypt en un archivo sqlite
def save_to_sqlite():
	pass

# Crea el socket TCP/IPa
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlaza el socket al puerto
server_address = ('localhost', 10009)
print('Server started on {} port {}'.format(*server_address))
sock.bind(server_address)

# Espera por una conexion
sock.listen(1)

BUFFER_SIZE = 1024

while True:
	print('Waiting for a connection')
	connection, client_address = sock.accept()

	try:
		print('connection from', client_address)
		p,q = get_prime(), get_prime()
		while p == q:
			q = get_prime()
		# Recibe la peticion y envia las llaves
		while True: 
			request = connection.recv(BUFFER_SIZE)
			print('request: ', request)
			if request.decode('utf-8') == 'REQUEST_PUBLIC_KEY':
				public_key, private_key, n = generate_keys(p, q)
				print ('Public key: ', public_key)
				print ('Private key: ', private_key)
				print ('n: ', n)
				public_key = str(public_key) + ':' + str(n) 
				package = str(sys.getsizeof(public_key)) + ':' + str(public_key)
				connection.sendall(bytes(package.encode('utf-8')))
				filename = receive_file(connection)
				decrypt_file(str(private_key), n, filename)
				save_to_sqlite()
			else:
				print('no data required')
				break

	finally:
		# Cierra la coneccion
		connection.close()