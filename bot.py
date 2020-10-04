from discord.ext import commands
import os
from cogs.config import settings

py = commands.Bot(command_prefix='!')
py.remove_command('help')


@py.command()
async def load(ctx, extension):
    if ctx.author.id == 280303417568788482:
        py.load_extension(f"cogs.{extension}")
        await ctx.send('Коги подгружены.')
    else:
        await ctx.send('Вы кто? Я вас не знаю.')


@py.command()
async def unload(ctx, extension):
    if ctx.author.id == 280303417568788482:
        py.unload_extension(f"cogs.{extension}")
        await ctx.send('Коги разгружены.')
    else:
        await ctx.send('Вы кто? Я вас не знаю.')


@py.command()
async def load(ctx, extension):
    if ctx.author.id == 280303417568788482:
        py.load_extension(f"cogs.{extension}")
        py.unload_extension(f"cogs.{extension}")
        await ctx.send('Коги перезагружены.')
    else:
        await ctx.send('Вы кто? Я вас не знаю.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        py.load_extension(f'cogs.{filename[:-3]}')

py.run(settings['TOKEN'])
