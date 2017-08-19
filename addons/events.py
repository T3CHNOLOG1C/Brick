#!/usr/bin/env python3

import configparser
import json
from asyncio import sleep 

import discord
import feedparser
from discord.ext import commands

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
        elif param == "list":
            await self.bot.say("__List of events :__\n\n- new_releases : {}".format(
                    "**Active**" if self.new_releases_active else "*Inactive*"))
        else:
            await self.bot.say("This event doesn't exist!"
                                + " Use `toggleevent list` to list every event.")

    async def new_releases(self):
        """
        Check for new GitHub releases of specified repositories
        """
        await self.bot.wait_until_ready()
        while self.new_releases_active:
            for owner, repo in self.repos.items():
                releases = feedparser.parse(
                    ("https://github.com/{}/{}/releases.atom".format(owner, repo))
                )
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
                        # Dirty but works
                        tag = permalink.split('/tag/')[1]
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

            await sleep(60)


def setup(bot):
    bot.add_cog(Events(bot))
