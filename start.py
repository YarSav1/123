from multiprocessing import Process
from discord.ext import commands

from moderation.ban import banned
from moderation.clear import clr
from moderation.unban import unbanned
from razgovor.chat import chat
from razgovor.help import helps

print('Начался запуск бота.')
client = commands.Bot(command_prefix='!')

words = ['ys', 'ны']

if __name__ == '__main__':
    p1 = Process(target=banned)
    p1.start()

print('Все компоненты загружены, бот почти загрузился.')


@client.event
async def on_message(message):
    msg = message.content.lower()

    if msg in words:
        await message.channel.send('Дада, я тута!')


@client.event
async def on_ready():
    print('Бот запущен.')


client.run("NzM3MjYwODIyNjY0OTcwMjYx.Xx6xpQ.MxDIJbMTFPL4qScZ68Vwt7zopco")
