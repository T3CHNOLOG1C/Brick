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
                await ctx.send("Please mention a user.")
                return
            await member.kick()
            await ctx.send("I've kicked {}.".format(member))
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")
            
    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def multikick(self, ctx, *, members):
        """Kick multiple members. (Staff Only)"""
        try:
            mention_check = ctx.message.mentions[0]
        except IndexError:
            await ctx.send("Please mention at least one user.")
            return
        for member in ctx.message.mentions:
            try:
                await member.kick()
                await ctx.send("Kicked {}.".format(member))
            except discord.errors.Forbidden:
                await ctx.send("💢 Couldn't kick {}".format(member))

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, member=""):
        """Ban a member. (Staff Only)"""
        owner = ctx.message.guild.owner
        if len(ctx.message.mentions) == 0:
            if ctx.message.author == owner:
                await ctx.send("Yes daddy t3ch?")
            else:
                await ctx.send("Please mention a user.")
        else:
            try:
                member = ctx.message.mentions[0]
                await member.ban(delete_message_days=0)
                await ctx.send("I've banned {}.".format(member))
            except discord.errors.Forbidden:
                await ctx.send("💢 I dont have permission to do this.")

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True)
    async def multiban(self, ctx, *, members):
        """Ban many members. (Staff Only)"""

        try:
            mention_check = ctx.message.mentions[0]
        except IndexError:
            await ctx.send("Please mention a user.")
            return
        for member in ctx.message.mentions:
            try:
                await member.ban(delete_message_days=0)
                await ctx.send("Banned {}.".format(member))
            except discord.errors.Forbidden:
                await ctx.send("💢 Couldn't ban {}".format(member))

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
