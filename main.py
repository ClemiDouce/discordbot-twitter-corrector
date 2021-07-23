import discord

client = discord.Client()


@client.event
async def on_ready():
    print("i'm ready !")


@client.event
async def on_message(message):
    if "twitter.com" in message.content and not message.author.bot:
        print('time to correct that shit')
        text = message.content
        position = text.find("twitter.com")
        final_string = text[:position] + "fx" + text[position:]
        await message.channel.send(f"{message.author.display_name} a posté ceci {final_string}")
        await message.delete()
    else:
        print("c'est bon, tu peux passer")


client.run("ODY4MDUwNDA2NTg3MTM4MDY4.YPqA8A.39CXdgzjJDAGob8Q4gUCcGtiC7k")