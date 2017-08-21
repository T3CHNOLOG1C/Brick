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
        
    @commands.command(pass_context=True)
    async def togglechannel(self, ctx, channel):
        """Toggle access to some hidden channels"""
        user = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if channel == "nsfw":
            if self.bot.nsfw_role in user.roles:
                await self.bot.remove_roles(user, self.bot.nsfw_role)
                await self.bot.send_message(self.bot.nsfw_channel, "{} left this channel.".format(user.mention))
            else:
                await self.bot.add_roles(user, self.bot.nsfw_role)                                             
                await self.bot.send_message(self.bot.nsfw_channel, "{} joined this channel.".format(user.mention))  

def setup(bot):
    bot.add_cog(Misc(bot))
