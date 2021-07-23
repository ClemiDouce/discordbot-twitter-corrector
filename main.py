from discord.ext import commands
import os

bot = commands.Bot(command_prefix='!')

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

bot.run(os.environ.get("bot-token"))
