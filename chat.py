from discord.ext import commands

client = commands.Bot(command_prefix='!')
privet = [ 'vsem privet!', 'vsem privet !', 'vsem privet.', 'vsem privet',
           'привет', 'привет!', 'привет !', 'привет.',
           'ку!' 'ку !' 'ку.' 'ку'
           'здарова!' 'здарова !' 'здарова.' 'здарова']
poka = [ 'lan poka', 'пока!', 'пока !', 'пока', 'лан пока']
voprosi = ['что здесь делать?', 'что здесь делать ?', 'что здесь делать', 'какие команды тут есть?',
           'команды', 'что может бот?', 'что может бот ?', 'что может бот']


def chat():
    @client.event
    async def on_message(message):
        msg = message.content.lower()
        if msg in voprosi:
            await message.channel.send('Пропиши команду и узнай мои возможности - !help')
        if msg in privet:
            await message.channel.send('Приветули!')
        if msg in poka:
            await message.channel.send('Пока! Еще увидимся, удачи!')

    client.run("NzM3MjYwODIyNjY0OTcwMjYx.Xx6xpQ.MxDIJbMTFPL4qScZ68Vwt7zopco")
