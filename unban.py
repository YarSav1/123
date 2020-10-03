import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')
client.remove_command('help')


def unbanned():
    @client.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def unban(ctx, *, member):

        await ctx.channel.purge(limit=1)

        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            emb = discord.Embed(titile='Разбан', colour=discord.Color.blurple())
            user = ban_entry.user

            await ctx.guild.unban(user)
            emb.set_author(name=member.name, icon_url=member.avatar_url)
            emb.add_field(name="Разбанен участник сервера.", value='Разбанен: {}'.format(member.mention))
            emb.set_footer(text='Разбанен пользователем: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)

            await ctx.send(embed=emb)

            return
        client.run("NzM3MjYwODIyNjY0OTcwMjYx.Xx6xpQ.MxDIJbMTFPL4qScZ68Vwt7zopco")
