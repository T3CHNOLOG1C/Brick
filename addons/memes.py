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

def setup(bot):
    bot.add_cog(Memes(bot))