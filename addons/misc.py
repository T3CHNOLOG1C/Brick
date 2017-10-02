#!/usr/bin/env python3.6

import datetime

import discord
from discord.ext import commands

class Misc:
    """
    Miscellaneous commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))
        
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""

        # https://github.com/appu1232/Discord-Selfbot/blob/master/cogs/misc.py#L595
        msgtime = ctx.message.created_at.now()
        await (await self.bot.ws.ping())
        now = datetime.datetime.now()
        ping = now - msgtime
        return await ctx.send(":ping_pong:! Response Time: {} ms".format(str(ping.microseconds / 1000.0)))

    @commands.command(pass_context=True, aliases=['mc'])
    async def membercount(self, ctx):
        """Prints current member count"""

        return await ctx.send(str(self.bot.guild.name)+" currently has " + str(len(self.bot.guild.members)) + " members!")
    
    @commands.command()
    async def about(self, ctx):
        """About Brick."""

        return await ctx.send("View my source code here: https://github.com/T3CHNOLOG1C/Brick")
        
    @commands.command(pass_context=True)
    async def togglechannel(self, ctx, channel):
        """Toggle access to some hidden channels"""

        user = ctx.message.author
        await ctx.message.delete()

        if self.bot.mcubrick_role in user.roles:
            return await ctx.send("This channel doesn't exist!") # (͡° ͜ʖ ͡°)
        
        if channel == "nsfw":
            if self.bot.no_nsfw_role in user.roles:
                return await ctx.send("You are banned from the NSFW channels!")
            
            if self.bot.nsfw_role in user.roles:
                await user.remove_roles(self.bot.nsfw_role)
                '''await self.bot.nsfw_channel.send("{} left this channel.".format(user.mention))'''
            else:
                await user.add_roles(self.bot.nsfw_role)                                             
                '''await self.bot.nsfw_channel.send("{} joined this channel.".format(user.mention))'''

def setup(bot):
    bot.add_cog(Misc(bot))
