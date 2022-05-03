import discord
import requests
import sys
import json
import os

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

client = discord.Client()
guild = discord.Guild


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = await client.fetch_channel(968339724144111679)
    count = 0
    message = None
    async for m in channel.history(limit=20):
        if count == 0:
            message = m
            count+=1
        await m.delete()

    if message is not None:
        print('Message fetched')
        #await message.channel.send('Message recieved!')
    

        image_url = message.attachments[0].url

        img_data = requests.get(image_url).content
        with open(resource_path(secrets['IMAGE_DOWNLOAD_PATH']), 'wb') as handler:
            handler.write(img_data)
    else:
        print('no messages')
    await client.close()
    
client.run(secrets['DISCORD_API_KEY'])
