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
    @commands.command()
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
    @commands.command()
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
    @commands.command()
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
    @commands.command()
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

    # NSFW-MODERATION COMMANDS

    @commands.group()
    async def nsfw(self, ctx):
        """NSFW moderation commands"""

        if ctx.invoked_subcommand is None:
            return await ctx.send("`Missing requirements. Please use .help nsfw`")

    async def checkNsfwModPerms(self, ctx):
        """Check if the member using a NSFW moderation command has the permission to do so."""

        if not ctx.message.author.permissions_in(self.bot.nsfw_channels).manage_messages:
            await ctx.send("{} You don't have permission to use this command.".format(ctx.message.author.mention))
            return(False)
        if ctx.message.mentions[0].permissions_in(self.bot.nsfw_channels).manage_messages:
            await ctx.send("{} You cannot use NSFW moderation commands on other NSFW mods!".format(ctx.message.author.mention))
            return(False)
        return(True)


    @nsfw.command(name="mute")
    async def nsfw_mute(self, ctx, member):
        """Prevent someone from sending messages in NSFW channels (NSFW mods only)"""

        has_perms = await self.checkNsfwModPerms(ctx)
        if not has_perms:
            return

        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")
        
        if self.bot.nsfw_muted_role in member.roles:
            return await ctx.send("{} is already muted!".format(member))

        try:
            await member.add_roles(self.bot.nsfw_muted_role, reason="Muted in the nsfw channels by {}.".format(
                ctx.message.author
                ))
            await ctx.send("{} can no longer speak in NSFW channels!".format(member))
            try:
                await member.send("You have been muted from the SSS NSFW channels. You will be DM'ed when a mod unmutes you.\n**Do not ask mods to unmute you, as doing so might extend the duration of the mute!**")
            except:
                pass
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")
        

    @nsfw.command(name="unmute")
    async def nsfw_unmute(self, ctx, member):
        """Allow someone to send messages in NSFW channels again (NSFW mods only)"""

        has_perms = await self.checkNsfwModPerms(ctx)
        if not has_perms:
            return

        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.nsfw_muted_role not in member.roles:
            return await ctx.send("{} isn't muted!".format(member))

        try:
            await member.remove_roles(self.bot.nsfw_muted_role, reason="Unmuted in the NSFW channels by {}.".format(
                ctx.message.author
                ))
            await ctx.send("{} can now speak again in NSFW channels!".format(member))
            try:
                await member.send("You have been unmuted from the SSS NSFW channels.")
            except:
                pass
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")


    @nsfw.command(name="kick")
    async def nsfw_kick(self, ctx, member):
        """
        Kick someone from the NSFW channels.
        They can rejoin with .togglechannel nsfw
        """

        has_perms = await self.checkNsfwModPerms(ctx)
        if not has_perms:
            return

        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.nsfw_role not in member.roles:
            return await ctx.send("{} isn't in the NSFW channels!".format(member))

        try:
            await member.remove_roles(self.bot.nsfw_role, reason="Kicked from the NSFW channels by {}.".format(
                ctx.message.author
                ))
            await ctx.send("Kicked {} from the NSFW channels. They can rejoin whenever with `.togglechannel nsfw`".format(member))
            try:
                await member.send("You have been kicked from the SSS NSFW channels.\nYou can join the channels back whenever you want with the ´.togglechannel` command.")
            except:
                pass
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")


    @nsfw.command(name="ban")
    async def nsfw_ban(self, ctx, member):
        """Ban someone from the NSFW channels."""

        has_perms = await self.checkNsfwModPerms(ctx)
        if not has_perms:
            return

        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.no_nsfw_role in member.roles:
            return await ctx.send("{} is already banned from NSFW channels!".format(member))

        try:
            await member.remove_roles(self.bot.nsfw_role, reason="Banned from the NSFW channels by {}.".format(ctx.message.author))
            await member.add_roles(self.bot.no_nsfw_role, reason="Banned from the NSFW channels by {}.".format(ctx.message.author))
            await ctx.send("Banned {} from the NSFW channels.".format(member))
            try:
                await member.send("You have been banned from the SSS NSFW channels.\nThis ban does not expire.")
            except:
                pass
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")


def setup(bot):
    bot.add_cog(Moderation(bot))
