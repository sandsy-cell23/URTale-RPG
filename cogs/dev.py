import discord
from discord.ext import commands
from botTools.dataIO import fileIO
import time
from datetime import datetime
from botTools.dataIO import fileIO
import asyncio
import sys
import os

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
        
    @commands.command()
    @commands.is_owner()
    async def Global(self, ctx):
        info = fileIO("config/config.json", "load")
        if info["Global"] == "Disabled":
            info["Global"] = "Enabled"
            await ctx.send("Global Bot Up")
            fileIO("config/config.json", "save", info)
            return
        if info["Global"] == "Enabled":
            info["Global"] = "Disabled"
            await ctx.send("Global Bot Down")
            fileIO("config/config.json", "save", info)
            return
    @commands.command()
    @commands.is_owner()
    async def shut(self, ctx):
        quit()
        
    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.reply("Restarting...")
        await asyncio.sleep(3)
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
        
    @commands.command()
    async def private(self, ctx):
        with open('servers.txt','w') as file:
            info = fileIO("config/config.json", "load")
            info["member_count"] = 0
            for guild in self.bot.guilds:  
                file.write(f"---------------\nGuild Name: {guild.name}\n\nGuild Member Count: {guild.member_count}\n\nGuild ID: {guild.id}\n\n--------------")
            for guild in self.bot.guilds:
                info["member_count"] = info["member_count"] + guild.member_count
                print(f"---------------\nGuild Name: {guild.name}\n\nGuild Member Count: {guild.member_count}\n\nGuild ID: {guild.id}\n\n--------------")
                fileIO("config/config.json", "save", info)

        
        
    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, arg):
        guild = await self.bot.fetch_guild(arg)
        await guild.leave()
        await ctx.send(f":ok_hand: Left guild: {guild.name} ({guild.id})")
        
    @commands.command()
    @commands.is_owner()
    async def Update(self, ctx):
        info = fileIO("config/config.json", "load")
        info["member_count"] = 0
        for guild in self.bot.guilds:
            info["member_count"] = info["member_count"] + guild.member_count
            fileIO("config/config.json", "save", info)
        info2 = fileIO("config/config.json", "load")
        count = info2["member_count"]
        await ctx.send(f"I have **{count} Members** Now!")
        

def setup(bot):
    bot.add_cog(Dev(bot))