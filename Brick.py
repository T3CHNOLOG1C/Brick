import discord
import configparser
from discord.ext.commands import Bot
from discord.ext import commands

bot_prefix = "B, "
my_bot = Bot(command_prefix=bot_prefix)

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
rules = {
    'r1':'Rule 1: Being an asshole is okay, but know when to stop.',
    'r2':"Rule 2: No doxing or harassment, either of these will result in an immidiate ban.",
    'r3':"Rule 3: Spamming is only allowed in the dedicated spam channel, #mcu-brick.",
    'r4':"Rule 4: Keep NSFW content to #nsfw. You can gain access to it by using the command ``.togglechannel nsfw``",
    'r5':"Rule 5: Ask a staff member before posting invite links to things like servers on Discord, Skype groups, etc.",
    'r6':"Rule 6: Content pertaining to discussion in the voice channels and excessive or random bot commands should be kept to #voice-and-bot-cmds",
    'r7':"Rule 7: Trying to evade, look for loopholes, or stay borderline within the rules will be treated as breaking them."
}

@my_bot.event
async def on_message(message):
    if message.content.lower()[len(bot_prefix):] in rules:
        await my_bot.send_message(message.channel, rules[message.content.lower()[len(bot_prefix):]])

### Admin Commands ###

@commands.has_role('Staff')
@my_bot.command()
async def staffcmd(ctx):
    return await my_bot.say("test.")

### Meme Commands ###

@my_bot.command()
async def gudie(*args):
    return await my_bot.say("https://gudie.racklab.xyz/")

@my_bot.command()
async def rip(*args):
    return await my_bot.say("Press F to pay respects.")
    
@my_bot.command()
async def t3ch(*Args):
		return await my_bot.say("https://i.imgur.com/4kANai8.png")

my_bot.run(config['Main']['token']) 
