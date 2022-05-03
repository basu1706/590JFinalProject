from email import message
from matplotlib import image
from stegano import lsbset
from stegano import lsb
from stegano.lsbset import generators
import glob, random
from cryptography.fernet import Fernet

import discord
import sys
import json

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

image = prepare_command(sys.argv[1], secrets["ENCRYPTION_KEY"])
image.save('./secret_img/upload.png')