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

    async def memberDM(self, ctx, member, message):
        try:
            if len(ctx.message.attachments) > 0:
                attachments = " ".join(attachment.url for attachment in ctx.message.attachments)
                message = "{} {}".format(message, attachments)
            else:
                if message == '':
                    return await ctx.send("You cannot send empty messages!")
                else:
                    await ctx.message.delete()
            if len(message) > 2000:
                await member.send(message[:2000])
                await member.send(message[2000:])
            else:
                await member.send(message)
        except discord.errors.Forbidden:
            await self.bot.logs_channel.send("Couldn't send message to {}.".format(member.mention))

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def dm(self, ctx, member, *, message=''):
        """DM a user. (Staff Only)"""
        member = ctx.message.mentions[0]
        await self.memberDM(ctx, member, message)

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True)
    async def answer(self, ctx, *, message=''):
        """Answer to the latest DM (Staff Only)"""
        async for m in self.bot.brickdms_channel.history(limit=250):
                try:
                    if m.author == self.bot.user:
                        member = m.mentions[0]
                        break
                    else:
                        continue
                except IndexError:
                    continue
        await self.memberDM(ctx, member, message)

def setup(bot):
    bot.add_cog(Speak(bot))
