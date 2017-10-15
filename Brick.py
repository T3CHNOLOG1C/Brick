#!/usr/bin/env python3.6

import os
import configparser
import asyncio
import traceback
import json
import copy
from subprocess import call
from os import execv
from sys import argv


import discord
from discord.ext import commands

# Change to script's directory
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# Create database
os.makedirs("database", exist_ok=True)
if not os.path.isfile("database/github_releases.json"):
    with open("database/github_releases.json", "w") as f:
        f.write('{}')
if not os.path.isfile("database/warns.json"):
    with open("database/warns.json", "w") as f:
        f.write('{}')
if not os.path.isfile("database/ignored_users.json"):
    with open("database/ignored_users.json", "w") as f:
        f.write('{"users": []}')

bot_prefix = ["sudo ", "."]
bot = commands.Bot(command_prefix=bot_prefix, description="Brick, the New Secret Shack Service bot.", max_messages=10000)

# Eead config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Handle errors
# Taken from 
# https://github.com/916253/Kurisu/blob/31b1b747e0d839181162114a6e5731a3c58ee34f/run.py#L88
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        pass
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("{} You don't have permission to use this command.".format(ctx.message.author.mention))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        msg = await formatter.format_help_for(ctx, ctx.command)
        await ctx.send("{} You are missing required arguments.\n{}".format(ctx.message.author.mention, msg[0]))
    else:
        await ctx.send("An error occured while processing the `{}` command.".format(ctx.command.name))
        print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        botdev_msg = "Exception occured in `{0.command}` in {0.message.channel.mention}".format(ctx)
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))
        await bot.botdev_channel.send(botdev_msg + '\n```' + ''.join(tb) + '\n```')


@bot.event
async def on_error(ctx, event_method, *args, **kwargs):
    if isinstance(args[0], commands.errors.CommandNotFound):
        return
    print('Ignoring exception in {}'.format(event_method))
    botdev_msg = "Exception occured in {}".format(event_method)
    tb = traceback.format_exc()
    print(''.join(tb))
    botdev_msg += '\n```' + ''.join(tb) + '\n```'
    botdev_msg += '\nargs: `{}`\n\nkwargs: `{}`'.format(args, kwargs)
    await bot.botdev_channel.send(botdev_msg)
    print(args)
    print(kwargs)


@bot.event
async def on_ready():

    for guild in bot.guilds:
        bot.guild = guild

    # Roles

    bot.owner_role = discord.utils.get(guild.roles, name="Owner")
    bot.staff_role = discord.utils.get(guild.roles, name="Staff")
    bot.botdev_role = discord.utils.get(guild.roles, name="#botdev")
    bot.nsfw_mod_role = discord.utils.get(guild.roles, name="NSFW Mod")
    bot.nsfw_role = discord.utils.get(guild.roles, name="nsfw")
    bot.nsfw_muted_role = discord.utils.get(guild.roles, name="nsfw-muted")
    bot.no_nsfw_role = discord.utils.get(guild.roles, name="no-nsfw")
    bot.mcubrick_role = discord.utils.get(guild.roles, name="MCU-BRICK")
    bot.polyglot_role = discord.utils.get(guild.roles, name="polyglot")

    # Channels
    bot.announcements_channel = discord.utils.get(guild.channels, name="announcements")
    bot.botdev_channel = discord.utils.get(guild.channels, name="botdev")
    bot.brickdms_channel = discord.utils.get(guild.channels, name="brick-dms")
    bot.logs_channel = discord.utils.get(guild.channels, name="admin-logs")

    # Categories
    bot.nsfw_channels = discord.utils.get(guild.categories, name="nsfw")
    bot.staff_channels = discord.utils.get(guild.categories, name="staff")


    # Ignored users
    with open("database/ignored_users.json", "r") as f:
        ignored_users = json.load(f)["users"]
    bot.ignored_users = ignored_users


    # Load addons
    addons = [
        'addons.memes',
        'addons.misc',
        'addons.rules',
        'addons.online',
        'addons.moderation',
        'addons.events',
        'addons.speak',
     ]

    for addon in addons:
        try:
            bot.load_extension(addon)
        except Exception as e:
            print("Failed to load {} :\n{} : {}".format(addon, type(e).__name__, e))

    bot.all_ready = True

    print("Client logged in as {}, in the following guild : {}".format(bot.user.name, guild.name))
    
# Core commands

@bot.command(hidden=True)
async def unload(ctx, addon: str):
    """Unloads an addon."""
    dev = ctx.message.author
    if bot.botdev_role in dev.roles or bot.owner_role in dev.roles:
        try:
            addon = "addons." + addon
            bot.unload_extension(addon)
            await ctx.send('✅ Addon unloaded.')
        except Exception as e:
            await ctx.send('💢 Error trying to unload the addon:\n```\n{}: {}\n```'.format(type(e).__name__, e))

@bot.command(name='reload', aliases=['load'], hidden=True)
async def reload(ctx, addon : str):
    """(Re)loads an addon."""
    dev = ctx.message.author
    if bot.botdev_role in dev.roles or bot.owner_role in dev.roles:
        try:
            addon = "addons." + addon
            bot.unload_extension(addon)
            bot.load_extension(addon)
            await ctx.send('✅ Addon reloaded.')
        except Exception as e:
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

@bot.command(hidden=True, name="pull", aliases=["pacman"])
async def pull(ctx, pip=None):
    """Pull new changes from Git and restart.\nAppend -p or --pip to this command to also update python modules from requirements.txt."""
    dev = ctx.message.author
    if bot.botdev_role in dev.roles or bot.owner_role in dev.roles:
        await ctx.send("`Pulling changes...`")
        call(["git", "stash", "save"])
        call(["git", "pull"])
        call(["git", "stash", "clear"])
        pip_text = ""
        if pip == "-p" or pip == "--pip" or pip == "-Syu":
            await ctx.send("`Updating python dependencies...`")
            call(["python3.6", "-m", "pip", "install", "--user", "--upgrade", "-r",
                "requirements.txt"])
            pip_text = " and updated python dependencies"
        await ctx.send("Pulled changes{}! Restarting...".format(pip_text))
        execv("./Brick.py", argv)
    else:
        if "pacman" in ctx.message.content:
            await ctx.send("`{} is not in the sudoers file. This incident will be reported.`".format(ctx.message.author.display_name))
        else:
            await ctx.send("Only bot devs and / or owners can use this command")

@bot.command()
async def restart(ctx):
    """Restart the bot (Staff Only)"""
    dev = ctx.message.author
    if bot.botdev_role in dev.roles or bot.owner_role in dev.roles:
        await ctx.send("`Restarting, please wait...`")
        execv("./Brick.py", argv)
        
# Run the bot
bot.run(config['Main']['token'])
