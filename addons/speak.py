#!/usr/bin/python3.6

import discord
from discord.ext import commands

class Speak:
    """Give the bot a voice"""

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True)
    async def speak(self, ctx, destination, *, message):
        """Make the bot speak (Staff Only)"""
        await ctx.message.delete()
        if len(ctx.message.channel_mentions) > 0:
            channel = ctx.message.channel_mentions[0]
            await channel.send(message)

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def dm(self, ctx, message, *, mentions):
        """DM mentionned users. (Staff Only)
        Message has to be between quotes."""
        await ctx.message.delete()
        for member in ctx.message.mentions:
            try:
                await member.send(message)
            except discord.errors.Forbidden:
                await self.bot.logs_channel.send("Couldn't send message to {}.".format(member.mention))
    
    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def answer(self, ctx, *, message):
        """Answer to the latest DM (Staff Only)"""
        await ctx.message.delete()
        async for m in self.bot.brickdms_channel.history(limit=250):
                try:
                    member = m.mentions[0]
                    break
                except IndexError:
                    continue
        try:
            await member.send(message)
        except:
            await ctx.send("Couldn't answer to the latest dm.")

def setup(bot):
    bot.add_cog(Speak(bot))
