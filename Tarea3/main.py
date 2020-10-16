#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto import Random
from Crypto.Cipher import AES
import base64
import argparse
from sys import exit

# Variables

BLOCK_SIZE = 16
SEGMENT_SIZE = 128
KEY = "2SQf1WNQnxYleSmg"  # Debe ser de 16 caracteres
text_to_encrypt = "Text to encrypt"


def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(length)*length


def unpad(data):
    return data[:-ord(data[-1])]


def encrypt(message, passphrase):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(passphrase, AES.MODE_CFB, IV, segment_size=SEGMENT_SIZE)
    return base64.b64encode(IV + aes.encrypt(pad(message)))


def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(passphrase, AES.MODE_CFB, IV, segment_size=SEGMENT_SIZE)
    return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))


def generate_HTML_file(cipher_text):
    html_text = """<p>Este sitio contiene un mensaje secreto</p>"""
    html_div = """<div class="algorithm" id="%s"></div>""" % (cipher_text)

    html_file = open('index.html', 'w')
    html_file.write(html_text)
    html_file.write(html_div)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Permite cifrar un mensaje utilizando el algoritmo Rijndael"
    )

    parser.add_argument("-b", "--blocksize", dest="blocksize", type=int, default=16,
                        help="Tamaño del bloque (16, 24 o 32)")
    parser.add_argument("-s", "--segmentsize", dest="segmentsize", type=int, default=128,
                        help="Tamaño del segmento (128, 196 o 256 bits). Debe coincidir en bytes con el tamaño del bloque")
    parser.add_argument("-k", "--key", dest="key", type=str, default="2SQf1WNQnxYleSmg",
                        help="Llave para cifrar/descifrar el mensaje, debe tener la misma cantidad de caracteres que el tamaño del bloque")
    parser.add_argument("-t", "--text", dest="text",
                        type=str, help="Mensaje a cifrar")

    args = parser.parse_args()

    if (args.blocksize == 16 and args.segmentsize == 128 and len(args.key) == 16 or args.blocksize == 24 and args.segmentsize == 196 and len(args.key) == 24 or args.blocksize == 32 and args.segmentsize == 256 and len(args.key) == 32):
        BLOCK_SIZE = args.blocksize
        SEGMENT_SIZE = args.segmentsize
        if args.text:
            text_to_encrypt = args.text

        cipher_text = encrypt(text_to_encrypt, KEY)
        generate_HTML_file(cipher_text)
    else:
        print('Valores inválidos. Utilice el comand -h para obtener mayor información del scrypt.')
        exit()
