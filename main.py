import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print("i'm ready !")


@client.event
async def on_message(message):
    if "https://twitter.com/" in message.content and not message.author.bot:
        print('time to correct that shit')
        text = message.content
        position = text.find("twitter.com")
        final_string = text[:position] + "fx" + text[position:]
        await message.channel.send(f"{message.author.display_name} a posté ceci {final_string}")
        await message.delete()


client.run(os.environ.get("bot-token"))
