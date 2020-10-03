import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')
client.remove_command('help')


def clr():
    @client.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clear(ctx, amount=10):
        emb = discord.Embed(titile='Бан', colour=discord.Color.blue())
        await ctx.channel.purge(limit=amount)

        emb.set_author(name='Бот YS', icon_url=client.user.avatar_url)
        emb.add_field(name='Чистка чата.', value='Было очищенно ' + str(amount) + ' сообщений.')
        await ctx.send(embed=emb)
    client.run("NzM3MjYwODIyNjY0OTcwMjYx.Xx6xpQ.MxDIJbMTFPL4qScZ68Vwt7zopco")
