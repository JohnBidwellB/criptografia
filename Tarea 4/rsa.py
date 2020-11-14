import random
import socket
import sys
import tqdm
import os
import numpy as np

PRIME_LIMIT = 1000000000

# Check if number is prime
def is_prime(num):
	if num == 2:
		return True
	if num < 2 or num % 2 == 0:
		return False
	for n in range(3, int(num ** 0.5) + 2, 2):
		if num % n == 0:
			return False
	return True

# Return primer number
def get_prime(limit = PRIME_LIMIT):
	num = 0
	while True:
		num = random.randint(0,limit)
		if is_prime(num):
			break
	return num

# Calculate the greatest common divisor between two numbers
def greatest_common_divisor(a, b):
	while b != 0:
		a, b = b, a % b
	return a

# Calculate modular multiplicative inverse
def modular_multiplicative_inverse(e, phi):
	if e == 0:
		return (phi, 0, 1)
	else:
		g, y, x = modular_multiplicative_inverse(phi % e, e)
	return (g, x - (phi // e) * y, y)

# Public and Private Key generation
def generate_keys(p, q):
	if not (is_prime(p) and is_prime(q)):
		raise ValueError('Ambos numeros deben ser primos')
	elif p == q:
		raise ValueError('Ambos numeros deben ser distintos')

	# Compute n
	n = p * q

	# Compute phi
	phi = (p - 1) * (q - 1)

	# Calculate encryption key
	e = random.randrange(1, phi) # Choose an integer number
	g = greatest_common_divisor(e, phi) # Calculate greatest common divisor
	while g != 1: # Calculate until find coprime numbers
		e = random.randrange(1, phi) # Choose an integer number
		g = greatest_common_divisor(e, phi) # Calculate greatest common divisor


	# Calculate decryption key
	d = modular_multiplicative_inverse(e, phi)[1]
	d = d % phi
	if d < 0:
		d += phi

	# Return public key (e), private key (d) and n
	return (e, d, n)

# Desencripta los hashes RSA
def decrypt(private_key, n, cipher_text):
	# print('params', private_key, type(private_key), n, type(n), cipher_text, type(cipher_text))
	try: 
		#password = [chr((int(char) ** int(private_key)) % n) for char in cipher_text] 
		password = [chr(pow(ord(char), private_key, n)) for char in cipher_text]
		# print('PASS', password)
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

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10009)
print('Server started on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
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
		# Receive the request and send the keys
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
		# Clean up the connection
		connection.close()