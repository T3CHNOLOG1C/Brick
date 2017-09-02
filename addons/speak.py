#!/usr/bin/python3

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
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def answer(self, *, message):
        """Answer to the latest DM (Staff Only)"""

        async for m in self.bot.logs_from(channel=self.bot.brickdms_channel, limit=1):
            member = m.mentions[0]
        await self.bot.send_message(member, message)

def setup(bot):
    bot.add_cog(Speak(bot))