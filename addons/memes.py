#!/usr/bin/env python3.6

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
    async def gudie(self, ctx):
        """Follow the Gudie to become a l33t Corbenik hax0r."""
        return await ctx.send("https://gudie.racklab.xyz/")

    @commands.command()
    async def rip(self, ctx):
        """F"""
        msg = await ctx.send("Press F to pay respects.")
        await msg.add_reaction("🇫")

    @commands.command()
    async def t3ch(self, ctx):
        """Goddamn Nazimod"""
        return await ctx.send("https://i.imgur.com/4kANai8.png")

    @commands.command()
    async def bigsmoke(self, ctx):
        """Memes."""
        await ctx.send("http://i.imgur.com/vo5l6Fo.jpg\nALL YOU HAD TO DO WAS FOLLOW THE DAMN GUIDE CJ!")
 
    @commands.command()
    async def bigorder(self, ctx):
        """Memes."""
        await ctx.send("I'll have two number 9s, a number 9 large, a number 6 with extra dip, a number 7, two number 45s, one with cheese, and a large soda.")
 
    @commands.command()
    async def heil(self, ctx):
        """SIEG HEIL"""
        await ctx.send("HEIL T3CH!")
        
    @commands.command()
    async def lenny(self, ctx):
        """( ͡° ͜ʖ ͡°)"""
        await ctx.send("( ͡° ͜ʖ ͡°)")
        
def setup(bot):
    bot.add_cog(Memes(bot))
