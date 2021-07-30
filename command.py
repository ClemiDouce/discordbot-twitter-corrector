from discord.ext import commands
import requests
import json
import os

from utils import get_tweet_id

bot = commands.Bot(command_prefix='!')

header = {
    'Authorization': 'Bearer ' + os.environ.get('bearer-token')
}

@bot.event
async def on_ready():
    print('Ready')


@bot.command(name='fx')
async def video(ctx, arg: str):
    if "https://twitter.com/" in arg:
        print('time to correct that shit')
        text = arg
        position = text.find("twitter.com")
        final_string = text[:position] + "fx" + text[position:]
        await ctx.send(f"{ctx.author.display_name} a posté ceci {final_string}")
        await ctx.message.delete()


@bot.command(name='gallery')
async def media_gallery(ctx, arg: str):
    if "https://twitter.com/" in arg:
        link = f"https://api.twitter.com/2/tweets/{get_tweet_id(arg)}?expansions=attachments.media_keys&media.fields=preview_image_url,url"
        data = requests.get(link, headers=header)
        try:
            final_data = json.loads(data.text)
            media_list = final_data['includes']['media']
            for media in media_list:
                await ctx.send(media['url'])
            await ctx.send(f"Source : <{arg}>")
            await ctx.message.delete()
        except KeyError:
            await ctx.send("Aucun media dans ce tweet")


bot.run(os.environ.get("bot-token"))
