import os
import json

import discord
from dotenv import load_dotenv

from utils import get_tweet_info


load_dotenv()
TOKEN = os.getenv('bot-token')

HEADER = {
    'Authorization': 'Bearer ' + os.getenv('bearer-token')
}


class DiscordClient(discord.Client):
    async def on_ready(self):
        print('ready')

    async def on_message(self, message):
        if message.content.startswith('!gallery'):
            splitted = message.content.split()
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
            splitted = message.content.split()
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
