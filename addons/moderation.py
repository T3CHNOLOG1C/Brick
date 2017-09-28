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
            await self.bot.say("I've kicked {}.".format(member))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I dont have permission to do this.")
            
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def multikick(self, ctx, *, members):
        """Kick multiple members. (Staff Only)"""
        try:
            mention_check = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention at least one user.")
            return
        for member in ctx.message.mentions:
            try:
                await self.bot.kick(member)
                await self.bot.say("Kicked {}.".format(member))
            except discord.errors.Forbidden:
                await self.bot.say("💢 Couldn't kick {}".format(member))

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, member=""):
        """Ban a member. (Staff Only)"""
        owner = ctx.message.server.owner
        if ctx.message.author == owner:
            if len(ctx.message.mentions) == 0:
                await self.bot.say("Yes daddy t3ch?")
        elif len(ctx.message.mentions) > 0:
            try:
                member = ctx.message.mentions[0]
                await self.bot.ban(member)
                await self.bot.say("I've banned {}.".format(member))
            except discord.errors.Forbidden:
                await self.bot.say("💢 I dont have permission to do this.")
        else:
            await self.bot.say("Please mention a user.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def multiban(self, ctx, *, members):
        """Ban multiple members. (Staff Only)"""

        try:
            mention_check = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please mention a user.")
            return
        for member in ctx.message.mentions:
            try:
                await self.bot.ban(member)
                await self.bot.say("Banned {}.".format(member))
            except discord.errors.Forbidden:
                await self.bot.say("💢 Couldn't ban {}".format(member))

    @commands.command(pass_context=True)
    async def nsfw-mute(self, ctx, member):
        """Mute someone in the NSFW channels. (NSFW Mod Only)"""
        
        if self.bot.nsfw_mod_role not in ctx.author.roles:
            self.bot.say("You don't have permission.")
            return
        if len(ctx.message.mentions) == 1:
            await self.bot.add_roles(ctx.message.mentions[0], self.bot.no_nsfw_role)
        else:
            await self.bot.say("You can only mute 1 person at a time")


def setup(bot):
    bot.add_cog(Moderation(bot))
