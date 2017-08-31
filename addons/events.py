#!/usr/bin/env python3

import configparser
import json
import asyncio
import aiohttp
import datetime

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
            "3dsfug": "Anemone3DS",
            "TuxSH": "firmtool",
            "Steveice10": "FBI",
            "44670": "BootNTR",
            "xerpi": "firm_linux_loader",
            "LiquidFenrir": "MultiUpdater",
            "fincs": "new-hbmenu",
            "Robz8": "TWLoader",
            "ahezard": "nds-bootstrap",
            "Nanquitas": "BootNTR",
        }
        bot.loop.create_task(self.new_releases())
        print("{} addon loaded.".format(self.__class__.__name__))

    new_releases_active = True
    h_active = True

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def toggleevent(self, param):
        """
        Make events active or not
        """
        if param == "new_releases":
            if self.new_releases_active is True:
                self.new_releases_active = False
                await self.bot.say("Stopped checking for new github releases!")
            else:
                self.new_releases_active = True
                await self.bot.say("Started checking for new github releases!")

        elif param == "h":
            if self.h_active is True:
                self.h_active = False
                await self.bot.say("I will now stop responding to `h`.")
            else:
                self.h_active = True
                await self.bot.say("I will now start responding to `h`.")

        elif param == "list":
            await self.bot.say("__List of events :__\n\n- new_releases : {}\n\n- h : {}".format(
                    "**Active**" if self.new_releases_active else "*Inactive*", "**Active**" if self.h_active else "*Inactive*"))
        else:
            await self.bot.say("This event doesn't exist!"
                                + " Use `toggleevent list` to list every event.")

    async def new_releases(self):
        """
        Check for new GitHub releases of specified repositories
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed and self.new_releases_active:

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
                                await self.bot.send_message(
                                    self.bot.announcements_channel,
                                    "{} {} released: {}".format(repo, tag, permalink)
                                )

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

    async def on_message(self, message):
        if message.content == "h" and message.author != self.bot.user and self.h_active:
            await self.bot.send_message(message.channel, "h")


def setup(bot):
    bot.add_cog(Events(bot))
