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
            try:
                return await user.send("This channel doesn't exist!") # (͡° ͜ʖ ͡°)
            except:
                pass
        
        if channel == "nsfw":
            if self.bot.no_nsfw_role in user.roles:
                try:
                    return await user.send("You are banned from the NSFW channels!")
                except:
                    pass

            if self.bot.nsfw_role in user.roles:
                await user.remove_roles(self.bot.nsfw_role)
            else:
                await user.add_roles(self.bot.nsfw_role)
        elif channel == "multilingual":
            if self.bot.polyglot_role in user.roles:
                await user.remove_roles(self.bot.polyglot_role)
            else:
                await user.add_roles(self.bot.polyglot_role)
                try:
                    await user.send("Welcome to <#367766453270872064>! Please read the pinned rules before starting to chat in this channel. Thank you!")
                except:
                    pass

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, amount):
        """Clears a given amount of messages. (Mods only)"""

        channel = ctx.message.channel
        try:
            n = int(amount) + 1
        except ValueError:
            return await ctx.send("Please mention a valid amount of messages!")

        try:
            await channel.purge(limit=n)
            await ctx.send("🗑️ Cleared {} messages in this channel!".format(amount))
        except discord.errors.Forbidden:
            await ctx.say("💢 I don't have permission to do this.")

def setup(bot):
    bot.add_cog(Misc(bot))
