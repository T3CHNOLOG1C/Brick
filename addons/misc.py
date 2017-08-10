#!/usr/bin/env python3

import discord
from discord.ext import commands

class Misc:
    """
    Miscellaneous commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))
        
    @commands.command()
    async def ping(self):
        """Pong!"""
        return await self.bot.say("Pong!")

    @commands.command()
    async def about(self):
        """About Brick."""
        return await self.bot.say("View my source code here: https://github.com/T3CHNOLOG1C/Brick")

def setup(bot):
    bot.add_cog(Misc(bot))