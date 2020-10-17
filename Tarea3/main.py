#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto import Random
from Crypto.Cipher import AES
import base64
import argparse
from sys import exit

BLOCK_SIZE = 16
SEGMENT_SIZE = 128
KEY = "2SQf1WNQnxYleSmg"  # Debe ser de BLOCK_SIZE caracteres
text_to_encrypt = "Hola criptografía"


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
    html_text = """<p id="title">Este sitio contiene un mensaje secreto</p>"""
    html_div = """<div class="algorithm" id="%s"></div>""" % (cipher_text)
    html_decodedtext = """<div id="decodedText"></div>"""
    html_key = """<div class="algorithmKey" id="%s"></div>""" % KEY

    html_file = open('index.html', 'w')
    html_file.write(html_text)
    html_file.write(html_div)
    html_file.write(html_key)
    html_file.write(html_decodedtext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Permite cifrar un mensaje utilizando el algoritmo Rijndael"
    )
    parser.add_argument("-k", "--key", dest="key", type=str, default="2SQf1WNQnxYleSmg",
                        help="Llave para cifrar/descifrar el mensaje, debe tener 16 caracteres")
    parser.add_argument("-t", "--text", dest="text",
                        type=str, help="Mensaje a cifrar")

    args = parser.parse_args()

    if (len(args.key) == 16):
        KEY = args.key
        if args.text:
            text_to_encrypt = args.text

        cipher_text = encrypt(text_to_encrypt, KEY)
        generate_HTML_file(cipher_text)
    else:
        print('Valores inválidos. Utilice el comando -h para obtener mayor información del scrypt.')
        exit()
