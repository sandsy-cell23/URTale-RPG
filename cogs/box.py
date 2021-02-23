from PIL import Image,ImageFont,ImageDraw
import discord
from discord.ext import commands
import os
import textwrap
import random

class box(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
              
        
    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.guild)
    async def text(self, ctx, *, args):
        x = args
        if len(x) >= 90:
            await ctx.send("You gave alot of letters, Going under 80 is recomended")
            return
        number = random.randint(1, 999)
        offset = 53
        bg = Image.open('Image.png')
        font = ImageFont.truetype(f"Font.ttf", 30)
        text = args
        draw = ImageDraw.Draw(bg)
        textwrapped = textwrap.wrap(text, width=30)
        draw.text((offset,17), '\n'.join(textwrapped), font=font, fill="#ffffff")
        bg.save(f'box{number}.png')
        file = discord.File(f"box{number}.png")
        await ctx.send(file=file)
        os.remove(f"box{number}.png")
        

def setup(bot):
    bot.add_cog(box(bot))