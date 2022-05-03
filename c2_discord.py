import discord
import requests
import sys
import json

f = open('secrets.json')
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
        with open(secrets['IMAGE_DOWNLOAD_PATH'], 'wb') as handler:
            handler.write(img_data)
    else:
        print('no messages')
    await client.close()
    
client.run(secrets['DISCORD_API_KEY'])
