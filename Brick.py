import discord
import configparser
from discord.ext.commands import Bot
from discord.ext import commands

my_bot = Bot(command_prefix="B, ")

#read config.ini
config = configparser.ConfigParser()
config.read("token.ini")

@my_bot.event
async def on_read():
    print("Client logged in")

### Misc. Commands ###

@my_bot.command()
async def ping(*args):
    return await my_bot.say("Pong!")

@my_bot.command()
async def about(*args):
    return await my_bot.say("View my source code here: https://github.com/T3CHNOLOG1C/Brick")


### Rule Commands ###

@my_bot.command()
async def r1(*args):
    return await my_bot.say("Rule 1: Being an asshole is okay, but know when to stop.")

@my_bot.command()
async def r2(*args):
    return await my_bot.say("Rule 2: No doxing or harassment, either of these will result in an immidiate ban.")

@my_bot.command()
async def r3(*args):
    return await my_bot.say("Rule 3: Spamming is only allowed in the dedicated spam channel, #mcu-brick.")

@my_bot.command()
async def r4(*args):
    return await my_bot.say("Rule 4: Keep NSFW content to #nsfw. You can gain access to it by using the command ``.togglechannel nsfw``")

@my_bot.command()
async def r5(*args):
    return await my_bot.say("Rule 5: Ask a staff member before posting invite links to things like servers on Discord, Skype groups, etc.")

@my_bot.command()
async def r6(*args):
    return await my_bot.say("Rule 6: Content pertaining to discussion in the voice channels and excessive or random bot commands should be kept to #voice-and-bot-cmds")

@my_bot.command()
async def r7(*args):
    return await my_bot.say("Rule 7: Trying to evade, look for loopholes, or stay borderline within the rules will be treated as breaking them.")

### Meme Commands ###

@my_bot.command()
async def gudie(*args):
    return await my_bot.say("https://gudie.racklab.xyz/")

@my_bot.command()
async def rip(*args):
    return await my_bot.say("Press F to pay respects.")

my_bot.run(config['Main']['token']) 
