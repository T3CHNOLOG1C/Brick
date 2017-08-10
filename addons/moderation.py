#!/usr/bin/env python3

from os import execv
from sys import argv
from subprocess import call

import discord
from discord.ext import commands

class Moderation:
    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

@commands.has_permissions(kick_members=True)
@commands.command(pass_context=True)
async def kick(self, ctx, member):
    """Kick a member. (Staff Only)"""
    try:       
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention a user.")
            return
        await self.bot.kick(member)
        await self.bot.say("I've kicked the user.")
    except discord.errors.Forbidden:
        await self.bot.say("💢 I dont have permission to do this.")

@commands.has_permissions(ban_members=True)
@commands.command(pass_context=True)
async def ban(self, ctx, member):
    """Ban a member. (Staff Only)"""
    try:       
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention a user.")
            return
        await self.bot.ban(member)
        await self.bot.say("I've banned the user.")
    except discord.errors.Forbidden:
        await self.bot.say("💢 I dont have permission to do this.")

@commands.command(pass_context=True, hidden=True)
async def pull(self, ctx):
    """Pull new changes from Git and restart."""
    dev = ctx.message.author
    if self.bot.botdev_role in dev.roles or self.bot.owner_role in dev.roles:
        await self.bot.say("`Pulling changes...`")
        call(["git", "pull"])
        await self.bot.say("Pulled changes! Restarting...")
        execv("./Brick.py", argv)
    else:
        await self.bot.say("Only bot devs and / or owners can use this command")

@commands.has_permissions(administrator=True)
@commands.command()
async def restart(self):
    """Restart the bot (Staff Only)"""
    await self.bot.say("`Restarting, please wait...`")
    execv("./Brick.py", argv)

def setup(bot):
    bot.add_cog(Moderation(bot))