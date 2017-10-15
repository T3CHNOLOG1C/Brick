#!/usr/bin/env python3.6

import configparser
import json
import asyncio
import aiohttp
import datetime
from time import strftime

import discord
import feedparser
from discord.ext import commands
from bs4 import BeautifulSoup

class Events:
    """
    Handle specific events and manage automation.
    """

    def __init__(self, bot):
        self.bot = bot
        self.repos = {
            # Format: "Owner":"Repo",   (Respect Case for repo name!)
            "AuroraWright": "Luma3DS",
            "d0k3": "GodMode9",
            "BernardoGiordano": "PKSM",
            "joel16": "3DSident",
            "kitling": "ntrboot_flasher",
            "SciresM": "boot9strap",
            "TuxSH": "firmtool",
            "Steveice10": "FBI",
            "44670": "BootNTR",
            "xerpi": "firm_linux_loader",
            "LiquidFenrir": "MultiUpdater",
            "fincs": "new-hbmenu",
            "Robz8": "TWLoader",
            "ahezard": "nds-bootstrap",
            "Nanquitas": "BootNTR",
            "astronautlevel2": "Anemone3DS",
            "T3CHNOLOG1C": "Discord-ChromeOS",
            "T3CHNOLOG1C": "DiscordCanary-ChromeOS",
            "kekmaster97": "fefosheep",
            "BernardoGiordano": "Checkpoint",
        }
        print("{} addon loaded.".format(self.__class__.__name__))
    
    # Events
    new_releases_active = True
    receive_dms = True

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def toggleevent(self, ctx, param):
        """
        Make events active or not
        """
        if param == "new_releases":
            if self.new_releases_active is True:
                self.new_releases_active = False
                await ctx.send("Stopped checking for new github releases!")
            else:
                self.new_releases_active = True
                await ctx.send("Started checking for new github releases!")

        elif param == "receive_dms":
            if self.receive_dms is True:
                self.receive_dms = False
                await ctx.send("Received DMs will now be ignored")
            else:
                self.receive_dms = True
                await ctx.send("Received DMs will now be transmitted in <#353101401880264704>!")

        elif param == "list":
            await ctx.send("__List of events :__\n\n- new_releases : {}\n- receive_dms : {}".format(
                    "**Active**" if self.new_releases_active else "*Inactive*",
                    "**Active**" if self.receive_dms else "*Inactive*"
                    ))
        else:
            await ctx.send("This event doesn't exist! Use `toggleevent list` to list every event.")

    async def new_releases(self):
        """
        Check for new GitHub releases of specified repositories
        """
        await self.bot.wait_until_ready()
        while self.new_releases_active:

            timestamp = datetime.datetime.now()
            if timestamp.minute % 2 == 0 and timestamp.second == 0:

                for owner, repo in self.repos.items():
                    try:
                        with aiohttp.ClientSession() as session:
                            with aiohttp.Timeout(5):
                                async with session.get("https://github.com/{}/{}/releases.atom".format(owner, repo)) as r:
                                    feed = await r.text()
                    except:
                        continue
                    releases = feedparser.parse(feed)

                    try:
                        latest = releases['entries'][0]

                        with open("database/github_releases.json", "r") as f:
                            js = json.load(f)

                        if latest['updated'] <= js['{}/{}'.format(owner, repo)][0]:
                            continue
                        elif str(latest['id']) == js['{}/{}'.format(owner, repo)][1]:
                            js['{}/{}'.format(owner, repo)] = [
                                latest['updated'], latest['id']
                            ]
                            continue
                        else:
                            permalink = latest['link']
                            if "https://github.com" not in permalink:
                                permalink = "https://github.com{}".format(permalink)
                            # Dirty but works
                            tag = permalink.split('/tag/')[1]

                            # Check if this is a release and not a tag
                            with aiohttp.ClientSession() as session:
                                with aiohttp.Timeout(10):
                                    async with session.get(permalink) as r:
                                        html = await r.text()
                            soup = BeautifulSoup(html, 'lxml')
                            authorship = str(soup.find('p', attrs={'class': 'release-authorship'}))

                            if "released this" in authorship and "tagged this" not in authorship:
                                await self.bot.announcements_channel.send("{} {} released: {}".format(repo, tag, permalink))

                            js['{}/{}'.format(owner, repo)] = [
                                latest['updated'], latest['id']
                            ]
                            
                    except KeyError:

                        # Entry does not exist in database yet, so we create it
                        js['{}/{}'.format(owner, repo)] = [
                            latest['updated'], latest['id']
                        ]

                    except IndexError:
                        continue

                    with open("database/github_releases.json", "w") as f:
                        json.dump(js, f, indent=2, separators=(',', ':'))

            await asyncio.sleep(1)
    
    def formatMessage(self, message):
        """Build a nicely formatted string from a message we want to log"""

        message_id = "Edited: {}".format(message.id) if message.edited_at else message.id

        author = message.channel.recipient.mention

        content = message.content

        attachments = ' '.join([attachment.url for attachment in message.attachments])

        return("__**[{}]** **{}** {}:__\n\n{} {}".format(message_id, "📤 To" if message.author == self.bot.user else "📥 From", author, content, attachments))

    async def on_message(self, message):

        if isinstance(message.channel, discord.abc.PrivateChannel) and self.receive_dms and message.author.id not in self.bot.ignored_users:
            msg = self.formatMessage(message)
            if len(msg) > 2000:
                await self.bot.brickdms_channel.send(msg[:2000])
                await self.bot.brickdms_channel.send(msg[2000:])
            else:
                await self.bot.brickdms_channel.send(msg)
            
        # Delete double messages
        elif message.channel == self.bot.brickdms_channel:      
            i = 0
            async for m in self.bot.brickdms_channel.history(limit=5):
                if m.author != self.bot.user:
                    continue
                if i == 0:
                    i += 1
                    p = m.content
                    continue
                else:
                    if m.content == p:
                        await m.delete()
                        break
                    else:
                        p = m.content
                    continue

                      
        # auto kick on 15+ pings
        if len(message.mentions) > 15:
            embed = discord.Embed(description=message.content)
            await message.delete()
            await message.author.kick()
            await message.channel.send("{} was kicked for trying to spam ping users.".format(message.author))
            await self.bot.logs_channel.send("{} was kicked for trying to spam ping users.".format(message.author))
            await self.bot.logs_channel.send("", embed=embed)

    async def on_message_edit(self, old, message):

        if isinstance(message.channel, discord.abc.PrivateChannel) and self.receive_dms and message.author.id not in self.bot.ignored_users:
            msg = self.formatMessage(message)
            if len(msg) > 2000:
                await self.bot.brickdms_channel.send(msg[:2000])
                await self.bot.brickdms_channel.send(msg[2000:])
            else:
                await self.bot.brickdms_channel.send(msg)
                
        elif old.content != message.content:
            embed = discord.Embed(description=f"{message.author} has edited their message!")
            embed.add_field(name="Old", value=old.content)
            embed.add_field(name="New", value=message.content)
            await self.bot.logs_channel.send(embed=embed)

def setup(bot): 
    event_cog = Events(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(event_cog.new_releases())
    bot.add_cog(event_cog)
