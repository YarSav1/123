import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')
client.remove_command('help')


def banned():
    @client.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        emb = discord.Embed(titile='Бан', colour=discord.Color.red())
        await ctx.channel.purge(limit=1)

        await member.ban(reason=reason)

        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.add_field(name="Забанен участник сервера.", value='Забанен: {}'.format(member.mention))
        emb.set_footer(text='Забанен пользователем: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)

        await ctx.send(embed=emb)

    client.run("NzM3MjYwODIyNjY0OTcwMjYx.Xx6xpQ.MxDIJbMTFPL4qScZ68Vwt7zopco")
