import twitchio
from twitchio.ext import commands
import re
from configparser import ConfigParser
import pathlib

# Get bot.py's father path
path = pathlib.Path(__file__).parent.resolve().__str__()

# Get the account config from config.ini
config = ConfigParser()
config.read(path + "\config.ini")
config_fields = config["ANDRESITOSITOSES_ACCOUNT"]

# IMPORTANTE: el token se genera en este enlace: https://twitchapps.com/tmi/
comandos = ["hello", "reverse"]

# Create a commands.Bot class
class Bot(commands.Bot):

    def __init__(self): 
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=config_fields["access_token"],
                         prefix=config_fields["prefix"],
                         initial_channels=[config_fields["name"]],
                         client_secret=config_fields["client_secret"]) # Creo que no sirve para nada

    async def event_ready(self):
        'The bot is logged in and ready to chat and use commands...'
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
    
    async def event_message(self, message: twitchio.Message):
        'Display messages on console'
        try:
            print(f"(chat) {message.author.name}: {message.content}")
        except:
            pass
        await super().event_message(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        'Send a hello back!'
        await ctx.send(f'Hola {ctx.author.name}, no le hagas mucho caso al trastornado que ves por pantalla.')

    @commands.command()
    async def reverse(self, ctx: commands.Context):
        'Send the content in a reverse way'
        matches = re.match("!reverse (.*)", ctx.message.content)
        if matches:
            await ctx.send(matches.groups()[0][::-1])
        else:
            await ctx.send(f"{ctx.author.name}, personaje, tienes que enviar el mensaje que quieres ver al revés.")

    @commands.command()
    async def help(self, ctx: commands.Context):
        'Send a message with the list of available commands'
        last_pos = len(comandos) - 1
        mensaje = ""
        if last_pos == 0:
            mensaje = comandos[0]
        for index, c in enumerate(comandos):
            if index == 0:
                mensaje = c
            elif index == last_pos:
                mensaje = f"{mensaje} y {c}"
            else:
                mensaje = f"{mensaje}, {c}"

        await ctx.send(f"{ctx.author.name}, estos son los comandos disponibles: {mensaje}")


while True:
    bot = Bot()
    bot.run()