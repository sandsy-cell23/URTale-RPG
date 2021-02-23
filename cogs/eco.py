import discord
from discord.ext import commands
from botTools.dataIO import fileIO
import time
from datetime import datetime
import main
import random
from PIL import Image,ImageFont,ImageDraw
import os

starttime = time.time()

class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def gold(self, ctx):
        author = ctx.author
        info = fileIO("players/{}/info.json".format(author.id), "load")
        bal = info["gold"]
        await ctx.send(f"Your gold balance is \n\n**{bal}G**")
    
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stats(self, ctx):
        author = ctx.author
        await main._create_user(author)
        info = fileIO("players/{}/info.json".format(author.id), "load")
        if info["race"] and info["class"] == "None":
            await ctx.send("Please start your character using `u?start`")
            return
        maxexp = 100 * info["lvl"]
        #image creation
        ID = random.randint(0, 9999)
        bg = Image.open('stat.png')
        font = ImageFont.truetype(f"Font.ttf", 70)
        draw = ImageDraw.Draw(bg)
        name = f"“{author.name}”"
        level = info["lvl"]
        health = info["health"]
        max_health = info["max_health"]
        attack = info["damage"]
        defence = info["defence"]
        exper = info["exp"]
        armor = info["wearing"]
        weapon = info["equip"]
        gold = info["gold"]
        lv = f"{level}"
        hp = f"{health}/{max_health}"
        mxp = f"{maxexp}"
        at = f"{attack}"
        df = f"{defence}"
        exp = f"{exper}"
        w = f"{armor}"
        e = f"{weapon}"
        g = f"{gold}"
        #name
        draw.text((67,87), name, font=font)
        #level
        draw.text((145,200), lv, font=font)
        #attack
        draw.text((145,410), at, font=font)
        #defence
        draw.text((145,480), df, font=font)
        #max exp
        draw.text((560,480), mxp, font=font)
        #exp
        draw.text((530,410), exp, font=font)
        #health
        draw.text((150,260), hp, font=font)
        #weapon
        draw.text((270,610), e, font=font)
        #gold
        draw.text((210,765), g, font=font)
        #armor
        draw.text((240,675), w, font=font)
        bg.save(f"{ID}.png")
        file = discord.File(f"{ID}.png")
        await ctx.send(file=file)
        os.remove(f"{ID}.png")
        
        
        
    @commands.command()
    async def inv(self, ctx):
        author = ctx.author
        await main._create_user(author)
        message = ctx.message
        info = fileIO("players/{}/info.json".format(author.id), "load")
        if info["race"] and info["class"] == "None":
            await ctx.send("Please start your character using `{}start`".format(Prefix))
            return
        em = discord.Embed(
            description="**Your Inventory:\n\n\nGold: {}\nLootbags: {}\nHP Potions: {}\n\nItems\n+{}**".format(info["gold"], info["lootbag"], info["hp_potions"], "\n+ ".join(info["inventory"]))
        )
        
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Eco(bot))