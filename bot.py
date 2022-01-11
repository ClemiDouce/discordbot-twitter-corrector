import os
import json

import discord
from dotenv import load_dotenv

from utils import get_tweet_info
from image_utils import resize_img

# sticker_names = ['sticker', 'inconnu']

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

    async def display_to_gallery(self, message, link):
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

    async def on_message(self, message):
        splitted = message.content.split()

        if message.content.startswith('!gallery'):
            await self.display_to_gallery(message, splitted[1])

        # if len(message.attachments) > 0 and message.author.bot == False:
        #     if any([substring in message.attachments[0].filename for substring in sticker_names]):
        #         with io.BytesIO() as image_binary:
        #             image = await resize_img(message.attachments[0].url, self.scale_mode)
        #             image.save(image_binary, 'PNG')
        #             image_binary.seek(0)
        #             await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
        #         await message.delete()
        # else:
        #     for word in splitted:
        #         if "https://twitter.com/" in word:
        #             tweet_info = await get_tweet_info(word, HEADER)
        #             final_data = json.loads(tweet_info)
        #             if final_data['includes']['media'][0]['type'] in {'video', 'animated_gif'}:
        #                 text = word
        #                 position = text.find("twitter.com")
        #                 final_string = text[:position] + "fx" + text[position:]
        #                 await message.channel.send(f"{message.author.display_name} a posté ceci {final_string}")
        #                 await message.delete()


client = DiscordClient()
client.run(TOKEN)
