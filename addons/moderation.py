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
    async def ban(self, ctx, member):
        """Ban a member. (Staff Only)"""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await self.bot.say("Please mention a user.")
                return
            await self.bot.ban(member)
            await self.bot.say("I've banned {}.".format(member))
        except discord.errors.Forbidden:
            await self.bot.say("💢 I dont have permission to do this.")

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

    @commands.command(pass_context=True, hidden=True, name="pull", aliases=["pacman"])
    async def pull(self, ctx, pip=None):
        """Pull new changes from Git and restart.
        Append -p or --pip to this command to also update python modules from requirements.txt.
        """
        dev = ctx.message.author
        if self.bot.botdev_role in dev.roles or self.bot.owner_role in dev.roles:
            await self.bot.say("`Pulling changes...`")
            call(["git", "pull"])
            pip_text = ""
            if pip == "-p" or pip == "--pip" or pip == "-Syu":
                await self.bot.say("`Updating python dependencies...`")
                call(["python3.6", "-m", "pip", "install", "--user", "-r",
                    "requirements.txt"])
                pip_text = " and updated python dependencies"
            await self.bot.say("Pulled changes{}! Restarting...".format(pip_text))
            execv("./Brick.py", argv)
        else:
            if "pacman" in ctx.message.content:
                await self.bot.say("`{} is not in the sudoers file. This incident will be reported.`".format(ctx.message.author.display_name))
            else:
                await self.bot.say("Only bot devs and / or owners can use this command")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def restart(self):
        """Restart the bot (Staff Only)"""
        await self.bot.say("`Restarting, please wait...`")
        execv("./Brick.py", argv)

    @commands.has_role("Owner")
    @commands.command()
    async def massnickname(self, *, nickname):
        """Change everyone's nickname (Owners only)"""

        if len(nickname) > 32:
            await self.bot.say("Nickname must have 32 characters or less!")
        else:
            i = 0
            for member in self.bot.server.members:
                try:
                    await self.bot.change_nickname(member, nickname)
                    i += 1
                except discord.errors.Forbidden:
                    continue
            await self.bot.say("Changed nickname of {} members!".format(i))

    @commands.has_role("Owner")
    @commands.command()
    async def resetnicknames(self):
        """Reset everyone's nickname (Staff only)"""
        i = 0
        for member in self.bot.server.members:
            try:
                await self.bot.change_nickname(member, None)
                i += 1
            except:
                continue
        await self.bot.say("Reset nickname of {} members!".format(i))

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True)
    async def speak(self, ctx, destination, *, message):
        """Make the bot speak (Staff Only)"""
        await self.bot.delete_message(ctx.message)
        channel = ctx.message.channel_mentions[0]
        await self.bot.send_message(channel, message)

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def dm(self, ctx, message, *, mentions):
        """
        DM mentionned users. (Staff Only)
        Message has to be between quotes.
        Append --everyone at the end of this command to DM everyone.
        """
        if mentions == "--everyone":
            if self.bot.owner_role in ctx.message.author.roles:
                for member in self.bot.server.members:
                    if member != self.bot.user and member != ctx.message.author:
                        try:
                            await self.bot.send_message(member, message)
                        except discord.errors.Forbidden:
                            await self.bot.send_message(ctx.message.channel, "Couldn't send message to {}.".format(member.mention))
            else:
                await self.bot.say("Only the owners can DM everyone!")
        else:
            await self.bot.delete_message(ctx.message)
            for member in ctx.message.mentions:
                try:
                    await self.bot.send_message(member, message)
                except discord.errors.Forbidden:
                    await self.bot.send_message(ctx.message.channel, "Couldn't send message to {}.".format(member.mention))

def setup(bot):
    bot.add_cog(Moderation(bot))
