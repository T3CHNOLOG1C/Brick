#!/usr/bin/env python3

import configparser
import discord
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

### Misc Cmds

@my_bot.command()
async def ping(*args):
    """Pong!"""
    return await my_bot.say("Pong!")

@my_bot.command()
async def about(*args):
    """About Brick."""
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

### Admin Commands ###

@commands.has_permissions(kick_members=True)
@my_bot.command(pass_context=True)
async def kick(ctx, member):
    """Kick a member. (Staff Only)"""
    try:       
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention a user.")
            return
        await my_bot.kick(member)
        await my_bot.say("I've kicked the user.")
    except discord.errors.Forbidden:
        await my_bot.say("💢 I dont have permission to do this.")
    
### Meme Commands ###

@my_bot.command()
async def gudie(*args):
    """Follow the Gudie to become a l33t Corbenik hax0r."""
    return await my_bot.say("https://gudie.racklab.xyz/")

@my_bot.command()
async def rip(*args):
    """F"""
    return await my_bot.say("Press F to pay respects.")
    
@my_bot.command()
async def t3ch(*Args):
    """Goddamn Nazimod"""
    return await my_bot.say("https://i.imgur.com/4kANai8.png")

my_bot.run(config['Main']['token']) 