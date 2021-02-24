import dbl
import discord
from discord.ext import commands, tasks

import asyncio
import logging
import flask
import asyncio
import sys
from botTools.dataIO import fileIO
import threading
import datetime
import time
import psutil
import random
import urllib
import requests
import shutil
import copy
from copy import deepcopy

import glob
import os
import aiohttp

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = "DBLTOKEN"
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/dblwebhook', webhook_auth='dady2005', webhook_port=2737)

    # The decorator below will work only on discord.py 1.1.0+
    # In case your discord.py version is below that, you can use self.bot.loop.create_task(self.update_stats())


    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        print('Attempting to post server count')
        
        try:
            await self.dblpy.post_guild_count()
            print('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
        await asyncio.sleep(1800)
        
  

        # if you are not using the tasks extension, put the line below
    @commands.Cog.listener()
    async def on_ready(self):
      await self.bot.loop.create_task(self.update_stats())
      print("loopex")


    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received an upvote:", "\n", data, sep="")
        voter2 = data
        unq = random.randint(0, 9999999999)
        fileIO(f"vote{unq}.json", "save", voter2)
        info = fileIO(f"vote{unq}.json", "load")
        voter = await self.bot.fetch_user(info['user'])
        
        if not os.path.exists("players/{}".format(voter.id)):
            os.makedirs("players/{}".format(voter.id))
            new_account = {
            "name": voter.name,
            "race": "None",
            "class": "None",
            "health": 100,
            "damage": 0,
            "max_health": 100,
            "enemyhp": 50,
            "bosshp" : 50,
            "in_fight": 0,
            "lvl": 1,
            "resets" : 0,
            "enemieskilled": 0,
            "bosskilled": 0,
            "deaths": 0,
            "selected_enemy": "None",
            "selected_boss": "None",
            "exp": 0,
            "gold": 200,
            "lootbag": 0,
            "wearing": "Bandage",
            "defence": 0,
            "skills_learned": [],
            "inventory" : [],
            "inv_armor" : [],
            "equip": "None",
            "location": "Ruins",
            "roaming": "False",
            "pet": "None",
            "daily_block": 0,
            "rest_block": 0,
            "hp_potions": 4,
            "max_pot" : 12,
            }
            fileIO("players/{}/info.json".format(voter.id), "save", new_account)
        voinfo = fileIO("players/{}/info.json".format(voter.id), "load")
        
        
        
        message = f"Thanks **{voter.mention}** for voting!, you Received your reward!"
        channel = self.bot.get_channel(802219611340668968)
        await channel.send(message)
        voinfo["gold"] = voinfo["gold"] + 500
        fileIO("players/{}/info.json".format(voter.id), "save", voinfo)
        await voter.send("You got your reward! **+500G**")
        os.remove(f"vote{unq}.json")

   
        
    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received a test upvote:", "\n", data, sep="")
        voter2 = data
        unq = random.randint(0, 9999999999)
        fileIO(f"vote{unq}.json", "save", voter2)
        info = fileIO(f"vote{unq}.json", "load")
        voter = await self.bot.fetch_user(info['user'])
        
        
        
        if not os.path.exists("players/{}".format(voter.id)):
            os.makedirs("players/{}".format(voter.id))
            new_account = {
            "name": voter.name,
            "race": "None",
            "class": "None",
            "health": 100,
            "damage": 0,
            "max_health": 100,
            "enemyhp": 50,
            "bosshp" : 50,
            "in_fight": 0,
            "lvl": 1,
            "resets" : 0,
            "enemieskilled": 0,
            "bosskilled": 0,
            "deaths": 0,
            "selected_enemy": "None",
            "selected_boss": "None",
            "exp": 0,
            "gold": 200,
            "lootbag": 0,
            "wearing": "Bandage",
            "defence": 0,
            "skills_learned": [],
            "inventory" : [],
            "inv_armor" : [],
            "equip": "None",
            "location": "Ruins",
            "roaming": "False",
            "pet": "None",
            "daily_block": 0,
            "rest_block": 0,
            "hp_potions": 4,
            "max_pot" : 12,
            }
            fileIO("players/{}/info.json".format(voter.id), "save", new_account)
        voinfo = fileIO("players/{}/info.json".format(voter.id), "load")
        
        message = f"Thanks **{voter.mention}** for voting!, you Received your reward!!"
        channel = self.bot.get_channel(802219611340668968)
        await channel.send(message)
        
        voinfo["gold"] = voinfo["gold"] + 500
        fileIO("players/{}/info.json".format(voter.id), "save", voinfo)
        await voter.send("You got your reward! **+500G**")
        os.remove(f"vote{unq}.json")

   
   
        
        

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(TopGG(bot))
