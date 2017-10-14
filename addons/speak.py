#!/usr/bin/python3.6

import discord
from discord.ext import commands

class Speak:
    """Give the bot a voice"""

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))
        
    def find_user(self, user, ctx):
        found_member = self.bot.guild.get_member(user)
        if not found_member:
            found_member = self.bot.guild.get_member_named(user)
        if not found_member:
            try:
                found_member = ctx.message.mentions[0]
            except IndexError:
                pass
        if not found_member:
            return None
        else:
            return found_member

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True)
    async def speak(self, ctx, destination, *, message):
        """Make the bot speak (Staff Only)"""
        await ctx.message.delete()
        if len(ctx.message.channel_mentions) > 0:
            channel = ctx.message.channel_mentions[0]
            await channel.send(message)

    async def memberDM(self, ctx, found_member, message):
        try:
            if ctx.message.attachments:
                attachments = ""
                for attachment in ctx.message.attachments:
                    attachments.append('{} '.format(attachment.url))
                message = "{} {}".format(message, attachments)
            if len(message) > 2000:
                await found_member.send(message[:2000])
                await found_member.send(message[2000:])
            else:
                await found_member.send(message)
        except discord.errors.Forbidden:
            await self.bot.logs_channel.send("Couldn't send message to {}.".format(found_member.mention))

    # @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def dm(self, ctx, member, *, message=""):
        """DM a user. (Staff Only)"""
        await ctx.message.delete()
        found_member = self.find_user(member, ctx)
        await self.memberDM(ctx, found_member, message)

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def multidm(self, ctx, message="", *, mentions):
        """DM multiple users. (Staff Only)
        Message has to be between quotes, and before the mentions."""
        await ctx.message.delete()
        for members in ctx.message.mentions:
            found_member = self.find_user(member, ctx)
            await self.memberDM(found_member, message)
    
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def answer(self, ctx, *, message):
        """Answer to the latest DM (Staff Only)"""
        await ctx.message.delete()
        async for m in self.bot.brickdms_channel.history(limit=250):
                try:
                    if ctx.message.author == self.bot.user:
                        found_member = m.mentions[0]
                        break
                    else:
                        continue
                except IndexError:
                    continue
        await self.memberDM(found_member, message)

def setup(bot):
    bot.add_cog(Speak(bot))
