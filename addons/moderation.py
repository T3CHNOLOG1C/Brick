#!/usr/bin/env python3

import asyncio
import json
import time
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

    async def dm(self, member, message):
        """DM the user and catch an eventual exception."""
        try:
            await member.send(message)
        except:
            pass

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

    # WARN STUFF

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def warn(self, ctx, member, *, reason):
        """
        Warn members. (Staff Only)
        A user ID can be used instead of mentionning the user.
        - First warn : nothing happens, a simple warning
        - Second warn : kick
        - Third warn : muted for a day
        - Fourth warn : time banned for 3 days
        - Fifth warn : banned
        """
        
        author = ctx.message.author
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.staff_role in member.roles and not self.bot.owner_role in author.roles:
            return await ctx.send("You cannot warn other staff members!")
        elif self.bot.owner_role in member.roles:
            return await ctx.send("💢 I don't have the permission to do that!")
        
        with open("database/warns.json", "r") as f:
            js = json.load(f) # https://hastebin.com/ejizaxasav.scala
        
        id = str(member.id)
        if id not in js:
            amount_of_warns = 1
            js[id] = {"warns": []}
        else:
            amount_of_warns = len(js[id]["warns"]) + 1
        
        member_name = "{}#{}".format(member.name, member.discriminator)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        author_name = "{}#{}".format(author.name, author.discriminator)

        js[id]["amount"] = amount_of_warns
        js[id]["warns"].append({
            "name": member_name,
            "timestamp": timestamp,
            "reason": reason,
            "author": author_name,
            "author_id": author.id,
        })

        await ctx.send("🚩 I've warned {}. The user now has {} warns.".format(member, amount_of_warns))
        await self.dm(member, "You have been warned in SSS for the following reason :\n\n{}\n\n".format(reason))

        if amount_of_warns == 1:
            await self.dm(member, "This is your first warning. The next warning will automatically kick you from the server.")
        elif amount_of_warns == 2:
            await self.dm(member, "This is your second warning, so you've been kicked from the server. You can rejoin immediately, but please note that *the next warn will result in an automatic mute!*")
            await member.kick(reason="Second warn.")
        elif amount_of_warns == 3:
            await self.dm(member, "This is your third warning, so you are muted for 24 hours. Please note that **the next warn will result in an automatic temporary ban!")
            # Someone implement a mute command already
        elif amount_of_warns == 4:
            await self.dm(member, "This is your fourth and final warning. **__The next ban will result in an automatic permanent ban.__**")
            # Someone implement a timeban command already
            await member.ban(delete_message_days=0, reason="Fourth warn.")
        elif amount_of_warns >= 5:
            await self.dm(member, "You have reached your fifth warning. You are now permanently banned from this server.")
            await member.ban(delete_message_days=0, reason="Fifth warn.")

        with open("database/warns.json", "w") as f:
            json.dump(js, f, indent=2, separators=(',', ':'))

    @commands.command()
    async def listwarns(self, ctx):
        """
        List your own warns or someone else's warns.
        Only the staff can view someone else's warns
        """

        try:
            member = ctx.message.mentions[0]
            if self.bot.staff_role in ctx.message.author.roles:
                has_perms = True
            else:
                has_perms = False
        except IndexError:
            member = ctx.message.author
            has_perms = True
        if not has_perms:
            return await ctx.send("{} You don't have permission to list other member's warns!".format(ctx.message.author.mention))

        with open("database/warns.json", "r") as f:
            js = json.load(f)
        
        id = str(member.id)
        if id not in js:
            return await ctx.send("No warns found!")
        
        embed = discord.Embed(color=member.colour)
        embed.set_author(name="List of warns for {} :".format(member), icon_url=member.avatar_url)

        for nbr, warn in enumerate(js[id]["warns"]):
            content = "{}".format(warn["reason"])
            if ctx.message.channel in self.bot.staff_channels.channels:
                author = await self.bot.get_user_info(warn["author_id"])
                content += "\n*Warn author : {} ({})*".format(warn["author"], author.mention)
            embed.add_field(name="\n\n#{}: {}".format(nbr + 1, warn["timestamp"]), value=content, inline=False)
        
        await ctx.send("", embed=embed)
 
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clearwarns(self, ctx, member):
        """Clear all of someone's warns. (Staff only)"""
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        with open("database/warns.json", "r") as f:
            js = json.load(f)

        try:
            js.pop(str(member.id))
            await ctx.send("Cleared all of {}'s warns!".format(member.mention))
        except KeyError:
            return await ctx.send("This user doesn't have any warns!")


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
        try:
            if ctx.message.mentions[0].permissions_in(self.bot.nsfw_channels).manage_messages:
                await ctx.send("{} You cannot use NSFW moderation commands on other NSFW mods!".format(ctx.message.author.mention))
                return(False)
        except IndexError:
            await ctx.send("Please mention a user.")
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
            await self.dm(member, "You have been muted from the SSS NSFW channels. You will be DM'ed when a mod unmutes you.\n**Do not ask mods to unmute you, as doing so might extend the duration of the mute!**")

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
            await self.dm(member, "You have been unmuted from the SSS NSFW channels.")

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
            await ctx.send("Kicked {} from the NSFW channels. They can rejoin whenever with .togglechannel nsfw".format(member))
            await self.dm(member, "You have been kicked from the SSS NSFW channels.\nYou can join the channels back whenever you want with the `.togglechannel` command.")

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
            await self.dm(member, "You have been banned from the SSS NSFW channels.\nThis ban does not expire.")

        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")

    @nsfw.command(name="unban")
    async def nsfw_unban(self, ctx, member):
        """Ban someone from the NSFW channels."""

        has_perms = await self.checkNsfwModPerms(ctx)
        if not has_perms:
            return

        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.no_nsfw_role not in member.roles:
            return await ctx.send("{} isn't banned from NSFW channels!".format(member))

        try:
            await member.remove_roles(self.bot.no_nsfw_role, reason="Unbanned from the NSFW channels by {}.".format(ctx.message.author))
            await ctx.send("Unbanned {} from the NSFW channels.".format(member))
            await self.dm(member, "You have been unbanned from the SSS NSFW channels.")
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")
def setup(bot):
    bot.add_cog(Moderation(bot))
