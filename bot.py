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
        splitted = message.split()
        for word in splitted:
            if "https://twitter.com/" in word:
                tweet_info = await get_tweet_info(word, HEADER)
                final_data = json.loads(tweet_info)
                if final_data['includes'][0]['type']:
                    text = word
                    position = text.find("twitter.com")
                    final_string = text[:position] + "fx" + text[position:]
                    await message.channel.send(f"{message.author.display_name} a posté ceci {final_string}")
                    await message.delete()


client = DiscordClient()
client.run(TOKEN)
