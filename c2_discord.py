import discord
import requests
import sys

IMAGE_DOWNLOAD_PATH = './secret_img/downloaded.png'
DISCORD_API_KEY = 'OTY4MzM4MjA4MDA4MDU2OTQy.YmdZOw.bf6adJCQDrqlHPKOzn-k_nBb4fc'

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
        with open(IMAGE_DOWNLOAD_PATH, 'wb') as handler:
            handler.write(img_data)
    else:
        print('no messages')
    await client.close()
    
client.run(DISCORD_API_KEY)
