import logging
logging.basicConfig(level='INFO')

import sys
try:
    import json
    import asyncio
    import discord
    from discord.ext import commands
    print('All modules successfully imported.')
except ImportError:
    print('Importing librairies failed. Some of the librairies may be missing or corrupted')
    sys.exit

with open('./config.json', 'r') as cjson:
    config = json.load(cjson)

PREFIX = config["prefix"]
modules = config["modules"]
OWNER = config["owner_id"]
VERSION = config["version"]
TOKEN = os.environ["TOKEN"]

bot = commands.Bot(command_prefix=PREFIX)

bot.config = config
bot.ready = False

async def status():
    while True:
        names = [f'{PREFIX}help', 'on AP3RTURE',]
        for name in names:
            await bot.change_presence(activity=discord.Game(name=name))
            await asyncio.sleep(10)

print("""
            _  __                    _  
           | |/ /__ _ _ _  _ _  __ _| | 
           | ' </ _` | ' \| ' \/ _` |_| 
           |_|\_\__,_|_||_|_||_\__,_(_)

Kanna is connecting...""")

@bot.event
async def on_connect():
    print('Successfully connected !')

#@bot.event
#async def on_command_error(ctx, exception):
#    await ctx.send(f'The following error happened during operation : ```{exception}``` Please check your command and then retry.')

@bot.event
async def on_ready():
    loaded = 0
    bot.remove_command('help')
    for module in modules:
        try:
            logging.info('Loading %s', module)
            bot.load_extension(f'modules.{module}')
        except Exception:
            logging.exception('Failed to load %s', module)
    print('Logged in.')
    print('Username : ' + bot.user.name)
    print('ID : ' + str(bot.user.id))
    print('Discord.py version : ' + str(discord.__version__))
    print(f"Kanna version : {VERSION}")
    print(f'Command prefix : {PREFIX}')
    print('Press CTRL+C to exit...')
    bot.loop.create_task(status())

bot.run(TOKEN)
