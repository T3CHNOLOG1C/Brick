#!/usr/bin/env python3

import discord
from discord.ext import commands

class Memes:
    """
    ayy lmao
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    @commands.command()
    async def gudie(self):
        """Follow the Gudie to become a l33t Corbenik hax0r."""
        return await self.bot.say("https://gudie.racklab.xyz/")

    @commands.command()
    async def rip(self):
        """F"""
        msg = await self.bot.say("Press F to pay respects.")
        await self.bot.add_reaction(msg, "🇫")

    @commands.command()
    async def t3ch(self):
        """Goddamn Nazimod"""
        return await self.bot.say("https://i.imgur.com/4kANai8.png")

    @commands.command
    async def bigsmoke(self, ctx):
        """Memes."""
        await self.bot.say(ctx, "http://i.imgur.com/vo5l6Fo.jpg\nALL YOU HAD TO DO WAS FOLLOW THE DAMN GUIDE CJ!")
 
    @commands.command
    async def bigorder(self, ctx):
        """Memes."""
        await self.bot.say(ctx, "I'll have two number 9s, a number 9 large, a number 6 with extra dip, a number 7, two number 45s, one with cheese, and a large soda.")
 
def setup(bot):
    bot.add_cog(Memes(bot))
