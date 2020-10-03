import discord
from discord.ext import commands


client = commands.Bot(command_prefix='!')
client.remove_command('help')


def helps():
    @client.command(pass_context=True)
    async def help(ctx):
        emb = discord.Embed(title='Доступные команды всем', colour=discord.Color.green())

        emb.set_author(name='Я хороший бот YS', icon_url=client.user.avatar_url)

        emb.add_field(name='YS', value='Тут ли бот?')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')
        emb.add_field(name='!ХЗ', value='чтото делает')

        await ctx.send(embed=emb)

    client.run("NzM3MjYwODIyNjY0OTcwMjYx.Xx6xpQ.MxDIJbMTFPL4qScZ68Vwt7zopco")
