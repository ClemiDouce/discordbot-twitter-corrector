import io
import os
import json

import discord
from dotenv import load_dotenv

from utils import get_tweet_info
from image_utils import resize_img


load_dotenv()
TOKEN = os.getenv('bot-token')

HEADER = {
    'Authorization': 'Bearer ' + os.getenv('bearer-token')
}


class DiscordClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.scale_mode = 4

    async def on_ready(self):
        print('ready')

    async def on_message(self, message):
        splitted = message.content.split()
        if len(message.attachments) > 0 and message.author.bot == False:
            with io.BytesIO() as image_binary:
                image = await resize_img(message.attachments[0].url, self.scale_mode)
                image.save(image_binary, 'PNG')
                image_binary.seek(0)
                await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
            await message.delete()
            print(message.attachments)
        if message.content.startswith('!scalesize'):
            if splitted[1].isdigit():
                self.scale_mode = int(splitted[1])
                await message.channel.send(f"Scale changé a {self.scale_mode}")
        elif message.content.startswith('!gallery'):
            link = splitted[1]
            if "https://twitter.com/" in link:
                data = await get_tweet_info(link, HEADER)
                try:
                    final_data = json.loads(data)
                    media_list = final_data['includes']['media']
                    for media in media_list:
                        await message.channel.send(media['url'])
                    await message.channel.send(f"Source : <{link}>")
                    await message.delete()
                except KeyError:
                    await message.channel.send("Aucun media dans ce tweet")
        else:
            for word in splitted:
                if "https://twitter.com/" in word:
                    tweet_info = await get_tweet_info(word, HEADER)
                    final_data = json.loads(tweet_info)
                    if final_data['includes']['media'][0]['type'] in {'video', 'animated_gif'}:
                        text = word
                        position = text.find("twitter.com")
                        final_string = text[:position] + "fx" + text[position:]
                        await message.channel.send(f"{message.author.display_name} a posté ceci {final_string}")
                        await message.delete()


client = DiscordClient()
client.run(TOKEN)
