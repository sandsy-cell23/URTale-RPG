import discord
from discord.ext import commands

import glob
import json

from botTools.dataIO import fileIO

class box(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
              
    @commands.command(aliases=['lb'])
    @commands.cooldown(1, 1000, commands.BucketType.guild)
    async def leaderboard(self, ctx):
        filenames_of_all_users = glob.glob("players/*/*.json")
        users = []
        for filename in filenames_of_all_users:
            with open(filename) as file:
                users.append(json.load(file))

        users.sort(key=lambda user: user["gold"], reverse=True)

        output = ["**"]
        for i, user in enumerate(users, 1):
            output.append(f"{i}. {user['name']}: {user['gold']} G")
            if i == 10:
                break
        output.append("**")
        result = "\n".join(output)
        embed = discord.Embed(title="Gold Leadersboard:", description=f"```diff\n{result}\n```")
        await ctx.send(embed=embed)
        
        
    @commands.command(aliases=['fix'])
    @commands.is_owner()
    async def Fix(self, ctx):
        filenames_of_all_users = glob.glob("players/*/*.json")
        for filename in filenames_of_all_users:
            players = fileIO(filename, "load")
            players["selected_enemy"] = "None"
            players["in_fight"] = 0
            players["health"] = 100
            fileIO(filename, "save", players)
            print(filename)
        print("Done")
            
            
            
        

def setup(bot):
    bot.add_cog(box(bot))
   