import datetime
import random
import sqlite3

import discord
from discord.ext import commands

from cogs.config import settings

py = commands.Bot(command_prefix=settings['PREFIX'])
py.remove_command('help')

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

spisok = ['ты букашка_1', 'ты букашка_2', 'ты букашка_3', 'ты букашка_4']


@py.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT,
    id INT,
    cash BIGINT,
    rep INT,
    lvl INT,
    server_id INT   
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
    role_id INT,
    id INT,
    cost BIGINT    
    )""")

    for guild in py.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 1000, 0, 1, {guild.id})")
            else:
                pass
    connect.commit()
    print("Бот готов.")
    await py.change_presence(activity=discord.Game('TimDuk\'a'))
    await py.get_guild(733319589252956202).get_channel(759757682809765919).send("Я запустился, <@280303417568788482>")


@py.event
async def on_member_join(member):
    channel = py.get_channel(759757682809765919)
    await channel.send(embed=discord.Embed(description=f'Ку {member.mention}, ' + random.choice(spisok)))
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 1000, 0, 1, {member.guild.id})")
        connect.commit()
    else:
        pass


@py.command(aliases=['balance', 'cash'])
async def _balance(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)

    if member is None:
        await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                           description=f"""Баланс **{ctx.author.mention}** составляет **{cursor.execute
                                           ("SELECT cash FROM users WHERE id={}".format(ctx.author.id))
                                           .fetchone()[0]} :money_with_wings: **"""))
    else:
        await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                           description=f"""Баланс **{member.mention}** составляет **{cursor.execute
                                           ("SELECT cash FROM users WHERE id={}"
                                            .format(member.id)).fetchone()[0]} :money_with_wings: **"""))


@py.command(aliases=['give', 'дать'])
async def _award(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author.mention}**, не указан пользователь для выдачи средств.")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author.mention}**, не указана сумма начисления.")
        elif amount < 1:
            await ctx.send(f"**{ctx.author.mention}**, Укажите сумму более 1 :money_with_wings: ")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
            connect.commit()

            await ctx.send(f"Вам, {member.mention}, начислено **{amount}** :money_with_wings:")


@py.command(aliases=['take', 'забрать'])
async def _take(ctx, member: discord.Member = None, amount=None):
    if member is None:
        await ctx.send(f"**{ctx.author.mention}**, не указан пользователь для изъятия средств.")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author.mention}**, не указана сумма изъятия.")
        elif amount == 'all':
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connect.commit()

            await ctx.send(f"У {member.mention} изъяты все :money_with_wings:")
        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author.mention}**, Укажите сумму более 1 :money_with_wings: ")
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
            connect.commit()

            await ctx.send(f"У {member.mention} было изъято **{amount}** :money_with_wings:")


@py.command(aliases=['add-shop', 'add', 'добавить'])
async def _add_shop(ctx, role: discord.Role = None, cost: int = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете внести в магазин")
    else:
        if cost is None:
            await ctx.send(f"**{ctx.author}**, укажите стоимость для даннойй роли")
        elif cost < 0:
            await ctx.send(f"**{ctx.author}**, стоимость роли не может быть такой маленькой")
        else:
            cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
            connect.commit()

            await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                               description=f"""Роль успешно добавлена в магазин."""))


@py.command(aliases=['remove-shop', 'удалить'])
async def _remove_shop(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую нужно удалить из магазина")
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        connect.commit()

        await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                           description=f"""Роль успешно удалена из магазина."""))


@py.command(aliases=['shop', 'магазин'])
async def _shop(ctx):
    embed = discord.Embed(title='Магазин ролей')

    for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
        if ctx.guild.get_role(row[0]) is not None:
            embed.add_field(
                name=f"Стоимость **{row[1]} :money_with_wings:**",
                value=f"Вы приобрете роль {ctx.guild.get_role(row[0]).mention}",
                inline=False
            )
        else:
            pass

    await ctx.send(embed=embed)


@py.command(aliases=['buy', 'buy-role', 'купить'])
async def _buy(ctx, role: discord.Role = None):
    if role is None:
        await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете приобрести")
    else:
        if role in ctx.author.roles:
            await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль")
        elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > \
                cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
            await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки данной роли")
        else:
            await ctx.author.add_roles(role)
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(
                cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0],
                ctx.author.id))
            connect.commit()

            await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                               description=f"""Роль успешно приобретена."""))


@py.command(aliases=['rep', '+rep'])
async def _rep(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите участника сервера")
    else:
        if member.id == ctx.author.id:
            await ctx.send(f"**{ctx.author}**, вы не можете указать смого себя")
        else:
            cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
            connect.commit()

            await ctx.send(embed=discord.Embed(colour=discord.Color.green(),
                                               description=f"""Репутация игрока повышена."""))


@py.command(aliases=['leaderboard', 'lb', 'лидеры'])
async def _leaderboard(ctx):
    embed = discord.Embed(title='Топ 10', colour=discord.Color.blue())
    counter = 0

    for row in cursor.execute \
                ("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
        counter += 1
        embed.add_field(
            name=f' {counter} | `{row[0]}`',
            value=f'**Баланс: `{row[1]}`** :money_with_wings:',
            inline=False
        )

    await ctx.send(embed=embed)


timenow = datetime.datetime.now()
print(timenow.hour, ' - ', timenow.minute, ' - ', timenow.second)


if timenow.second == 0:
    py.get_guild(733319589252956202).get_channel(759757682809765919).send("123")


py.run(settings['TOKEN'])
