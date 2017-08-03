#!/usr/bin/env python3

import os
import configparser
import json
import requests
import wikipedia
import discord
from string import capwords
from urllib.parse import urlencode
from subprocess import call
from sys import argv
from os import execv
from discord.ext.commands import Bot
from discord.ext import commands

# Change to script's directory
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

bot_prefix = "B, "
my_bot = Bot(command_prefix=bot_prefix)

#read config.ini
config = configparser.ConfigParser()
config.read("config.ini")


### Init ###

@my_bot.event
async def on_ready():
    print("Client logged in")

    for server in my_bot.servers:
        my_bot.server = server

    # Roles
    my_bot.owner_role = discord.utils.get(server.roles, name="Owner")
    my_bot.botdev_role = discord.utils.get(server.roles, name="#botdev")

### Misc Cmds

@my_bot.command()
async def ping(*args):
    """Pong!"""
    return await my_bot.say("Pong!")

@my_bot.command()
async def about(*args):
    """About Brick."""
    return await my_bot.say("View my source code here: https://github.com/T3CHNOLOG1C/Brick")

@my_bot.command(pass_context=True, hidden=True)
async def pull(ctx):
    """Pull new changes from GitHub and restart."""
    dev = ctx.message.author
    if my_bot.botdev_role in dev.roles or my_bot.owner_role in dev.roles:
        await my_bot.say("`Pulling changes...`")
        call(["git", "pull"])
        await my_bot.say("Pulled changes! Restarting...")
        execv("./Brick.py", argv)
    else:
        await my_bot.say("Only bot devs and / or owners can use this command")

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
            await my_bot.say("Please mention a user.")
            return
        await my_bot.kick(member)
        await my_bot.say("I've kicked the user.")
    except discord.errors.Forbidden:
        await my_bot.say("💢 I dont have permission to do this.")

@commands.has_permissions(ban_members=True)
@my_bot.command(pass_context=True)
async def ban(ctx, member):
    """Ban a member. (Staff Only)"""
    try:       
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await my_bot.say("Please mention a user.")
            return
        await my_bot.ban(member)
        await my_bot.say("I've banned the user.")
    except discord.errors.Forbidden:
        await my_bot.say("💢 I dont have permission to do this.")

@commands.has_permissions(administrator=True)
@my_bot.command(pass_context=True)
async def restart():
    """Restart the bot (Staff Only)"""
    await my_bot.say("`Restarting, please wait...`")
    execv("./Brick.py", argv)

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

### Online search commands ###

@my_bot.command()
async def urban(*, term=None):
    """Lookup a term on Urban Dictionnary. If no term is specified, returns a random definition. Use a comma followed by a number to specify the definition that should be returned."""
    
    if term is None:
        r = requests.get("http://api.urbandictionary.com/v0/random")
    else:
        n = 1
        if "," in term:
            n = term.split(",", 1)[1]
            term = term.split(",", 1)[0]
        r = requests.get("http://api.urbandictionary.com/v0/define?term={}".format(term))
    
    js = r.json()

    try:
        if js["result_type"] != "no_results":
            resultFound = True
    except:
        resultFound = True
    if resultFound:
        try:
            if term is None:
                firstResult = js["list"][0]
            else:
                firstResult = js["list"][int(n)-1]
            word = firstResult["word"]
            definition = firstResult["definition"]
            example = firstResult["example"]
            author = firstResult["author"]
            permalink = firstResult["permalink"]
            thumbsup = firstResult["thumbs_up"]
            thumbsdown = firstResult["thumbs_down"]

            chars = ['[', ']', '\\r\\n', "\\n"]
            for c in chars:
                if c == chars[0] or c == chars[1]:
                    definition = definition.replace(c, '')
                    example = example.replace(c, '')
                elif c == chars[2] or c == chars [3]:
                    definition = definition.replace(c, '\n')
                    example = example.replace(c, '\n')

            if example != "":
                textExamples = example
            else:
                textExamples = "None"

            try:
                embed = discord.Embed(title="Definition of {}\n\n".format(word), colour=discord.Color.blue())
                embed.set_thumbnail(url="http://i.imgur.com/B1gZbQz.png")
                embed.url = permalink
                embed.description = definition + "\n"
                if textExamples != "None":
                    embed.add_field(name="__Example(s) :__", value=textExamples, inline=False)
                embed.add_field(name="Upvotes", value="👍 **{}**".format(thumbsup), inline=True)
                embed.add_field(name="Downvotes", value="👎 **{}**\n\n".format(thumbsdown), inline=True)
                embed.set_footer(text="Defined by {0}".format(author))
                await my_bot.say(embed=embed)
            except (discord.errors.Forbidden, discord.errors.HTTPException):
                await my_bot.say("**__Definition of {0}__**__ ({1})__\n\n\n".format(word, permalink) + definition + "\n\n" + "__Example(s) :__\n\n" + textExamples + "\n\n\n" + str(thumbsup) + " 👍\n\n" + str(thumbsdown) + " 👎\n\n\n\n" + "*Defined by " + author + "*")
        except ValueError:
            await my_bot.say("`Invalid syntax. If you want to specify which definition should be returned, use the following syntax :\n\".urban [term], [number]\"`")
        except IndexError:
            await my_bot.say("The specified definition does not exist! There are less than {} definitons for this term!".format(n))
    else:
        try:
            embed = discord.Embed(title="¯\_(ツ)_/¯", colour=discord.Color.blue())
            embed.url = "http://www.urbandictionary.com/define.php?term={}".format(term.replace(" ", "%20"))
            embed.description = "\nThere aren't any definitions for *{0}* yet.\n\n[Can you define it?](http://www.urbandictionary.com/add.php?word={1})\n".format(term, term.replace(" ", "%20"))
            embed.set_footer(text="Error 404", icon_url="http://i.imgur.com/w6TtWHK.png")
            await my_bot.say(embed=embed)
        except discord.errors.Forbidden:
            await my_bot.say("¯\_(ツ)_/¯\n\n\n" + "There are no definitions for *{}* yet\n\n".format(term) + "Can you define it ?\n( http://www.urbandictionary.com/add.php?word={} )".format(term.replace(" ", "%20")))

@my_bot.command(name='whats', aliases=["what", "what's"])
async def whats(*, term):
    """Defines / explains stuff"""

    #Read config for Google API Key
    config = configparser.ConfigParser()
    config.read("config.ini")
    try:
        apiKey = config['Google']['API_Key']
    except KeyError:
        await my_bot.say("You did not mention a Google kgsearch API Key in the config.ini file! Please set up one here : https://console.developers.google.com/project/_/apiui/credential")


    if term[0:2] == "a " and term != "a":
        term = term[2:]
    elif term[0:3] == "an " and term != "an":
        term = term[3:]
    elif term[0:5] == "is a " and term != "is a":
        term = term[5:]
    elif term[0:6] == "is an " and term != "is an":
        term = term[6:]
    elif term[0:3] == "is " and term != "is":
        term = term[3:]
    elif term[0:4] == "are " and term != "are" and term != "are you":
        term = term[4:]

    term = capwords(term)

    if term.lower() == "kai" or term.lower() == "mitchy":
        kai = await my_bot.get_user_info("272908611255271425")
        try:
            embed = discord.Embed(title="Kai", colour=discord.Color.blue())
            embed.set_thumbnail(url=kai.avatar_url)
            embed.description = "An edgy kid that spends too much time on tumblr, previously named mitchy, previously named sans-serif"
            await my_bot.say(embed=embed)
        except discord.errors.Forbidden:
            await my_bot.say("**__Kai :__**\n\nAn edgy kid that spends too much time on tumblr, previously named mitchy, previously named sans-serif")
    elif term.lower() == "ubuntu":
            embed = discord.Embed(title="Ubuntu", colour=discord.Color.blue())
            embed.set_thumbnail(url="http://i.imgur.com/B1gZbQz.png")
            embed.url = "http://www.urbandictionary.com/define.php?term=ubuntu"
            embed.description = "Ubuntu is an ancient african word, meaning \"I can't configure Debian\"" + "\n"
            embed.add_field(name="__Example :__", value="I installed Ubuntu yesterday, it was way more easier than Debian", inline=False)
            embed.set_footer(text="Defined by oSuperDaveo")
            try:
                await my_bot.say(embed=embed)
            except discord.errors.Forbidden:
                await my_bot.say("**__Ubuntu :__**\n\n{}\n\n__Example :__\nI installed Ubuntu yesterday, it was way more easier than Debian.\n\n*Defined by oSuperDaveo*".format(embed.description))
    elif term.lower() == "t3chnolog1c" or term.lower() == "t3ch":
        t3ch = await my_bot.get_user_info("208370244207509504")
        try:
            embed = discord.Embed(title="T3CHNOLOG1C", colour=discord.Color.blue())
            embed.set_thumbnail(url=t3ch.avatar_url)
            embed.description = "The cancerous retard that runs this server."
            await my_bot.say(embed=embed)
        except discord.errors.Forbidden:
            await my_bot.say("**__T3CHNOLOG1C :__**\n\nThe cancerous retard that runs this server.")
    elif term.lower() == "are you":
        return await my_bot.say("View my source code here: https://github.com/T3CHNOLOG1C/Brick")

    else:
        exception = False
        try:
            #Start wikipedia search
            wiki = wikipedia.page(term)
            permalink = "https://en.wikipedia.org/wiki/{}".format(term.replace(" ", "_"))
            embed = discord.Embed(title=term, colour=discord.Color.blue())
            embed.url = permalink
            if wiki.summary[-13:] == "may refer to:":
                if len(wiki.content) > 1950:
                    embed.description = "{}...".format(wiki.content[0:1950])
                else:
                    embed.description = wiki.content
            else:
                if len(wiki.summary) > 1950:
                    embed.description = "{}...".format(wiki.summary[0:1950])
                else:
                    embed.description = wiki.summary
            embed.set_footer(text="From Wikipedia", icon_url="http://i.imgur.com/DO4wDN4.png")
            try: 
                await my_bot.say(embed=embed)
            except discord.errors.Forbidden:
                await my_bot.say("**__{}__**\n\n\n{}\n\n*Link : {}*".format(term, embed.description, permalink))
            #Images soon

        except wikipedia.exceptions.PageError:
            exception = True
            disambig = False
        except wikipedia.exceptions.DisambiguationError:
            exception = True
            disambig = True
        if exception is True:
            #Start Google Graph Knowledge search
            params = {
                'query': term,
                'limit': 1,
                'indent': True,
                'key': apiKey,
            }
            url = "https://kgsearch.googleapis.com/v1/entities:search?{}".format(urlencode(params))
            r = requests.get(url)
            js = r.json()

            try:
                if js["itemListElement"]:
                    js = js["itemListElement"][0]["result"]

                    name = js["name"]

                    embed = discord.Embed(title=name, colour=discord.Color.blue())
                    
                    try:
                        briefDescription = js["description"]
                        isBrieflyDetailed = True
                    except KeyError:
                        briefDescription = "No brief description available."
                        isBrieflyDetailed = False

                    try:
                        detailedDescription = js["detailedDescription"]["articleBody"]
                        isDetailed = True
                        if detailedDescription[-1] == " " or detailedDescription[-1] == "\n":
                            detailedDescription = detailedDescription[:-1]
                    except KeyError:
                        isDetailed = False
                        detailedDescription = "No detailed description available."

                    try:
                        permalink = js["detailedDescription"]["url"]
                        embed.url = permalink
                    except KeyError:
                        permalink = "no permalink available." 

                    if isDetailed is True and isBrieflyDetailed is True:
                        embed.description = "\n{}\n\n\n*{}*\n".format(briefDescription, detailedDescription)
                    elif isDetailed is False and isBrieflyDetailed is True:
                        embed.description = "\n{}\n\n".format(briefDescription)
                    elif isDetailed is True and isBrieflyDetailed is False:
                        embed.description = "\n\n*{}*\n\n".format(detailedDescription)

                    
                    try:
                        image = js["image"]["contentUrl"]
                        embed.set_image(url=image)
                    except KeyError:
                        image = "No image available."

                    embed.set_footer(text="From Google Graph Knowledge", icon_url="http://i.imgur.com/2obljmu.png")
                
                    try:
                        await my_bot.say(embed=embed)
                    except discord.errors.Forbidden:
                        await my_bot.say("__**{}** ({})__\n\n{}\n\n\n*{}*\n\n{}\n".format(name, permalink, briefDescription, detailedDescription, image))

                    if disambig is True:
                        await my_bot.say("If this is not the definition you wanted, try being a bit more precise next time. {} can refer to many things!".format(term))
                else:
                    await my_bot.say("Sorry, none of my sources have an explanation for this term :(")
                    #Coming soon : WikiData and urban dictionnary support

            except KeyError:
                if js["error"]["code"] == 403: #Checks if API Key is specified
                    await my_bot.say("You did not mention a Google kgsearch API Key in the config.ini file! Please set up one here : https://console.developers.google.com/project/_/apiui/credential")
                elif js["error"]["code"] == 400: #Checks if API Key is valid
                    await my_bot.say("The mentioned Google kgsearch API Key is invalid! Please set up a correct API Key here : https://console.developers.google.com/project/_/apiui/credential")


my_bot.run(config['Main']['token']) 