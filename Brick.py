import discord
import configparser
from discord.ext.commands import Bot
from discord.ext import commands

my_bot = Bot(command_prefix="!")

#read config.ini
config = configparser.ConfigParser()
config.read("token.ini")

@my_bot.event
async def on_read():
    print("Client logged in")

@my_bot.command()
async def ping(*args):
    return await my_bot.say("Pong!")


my_bot.run(config['Main']['token']) 
