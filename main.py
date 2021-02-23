import asyncio
import sys
from botTools.dataIO import fileIO
import threading
import datetime
import time
import psutil
import urllib
import shutil
import copy
import random
import ffmpeg
from random import choice
from copy import deepcopy
from datetime import datetime
import dbl
from discord import Embed

import glob
import os
import aiohttp
import discord
from discord.ext import commands

starttime = time.time()

VS = 1.2

config_location = fileIO("config/config.json", "load")
Shards = config_location["Shards"]
Prefix = config_location["Prefix"]

bot = commands.AutoShardedBot(shard_count = Shards, command_prefix=Prefix)
bot.launch_time = datetime.utcnow()

bot.remove_command('help')

bot.load_extension('jishaku')
    
@bot.command()
async def ping(ctx):
    await ctx.reply(f"Pong!🏓 My Latency Was \n**{round(bot.latency * 1000)}ms**!")
    
@bot.command()
async def uptime(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"My Uptime is:\n\n```py\n{days}d, {hours}h, {minutes}m, {seconds}s```")

#-----------------------------------------------------------------#
#-------------------------------RPG-------------------------------#
#-----------------------------------------------------------------#

#--------------------------------------------------------------------------#
#-------------------------------BOT COMMANDS-------------------------------#
#--------------------------------------------------------------------------#
@bot.command()
async def start(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    message = ctx.message
    await _create_user(author)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        info["race"] = "Normal"
        fileIO("players/{}/info.json".format(author.id), "save", info)
        await _pick_class(ctx)
    else:
        await ctx.reply("You're already setup.")

        #Setup done
        
        #Normal Fight!
@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def fight(ctx):
    author = ctx.author
    message = ctx.message
    await _create_user(author)
    check = fileIO("config/config.json", "load")
    info = fileIO("players/{}/info.json".format(author.id), "load")
    einfo = fileIO("core/enemies/enemies.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    if info["in_fight"] == 1:
        await ctx.send("You are already in a fight!")
        return
    if info["race"] and info["class"] == "None":
        await ctx.send(f"{author.mention} please start your character using u?start\n\n**Reseted for armor and consumables update**")
        return
    if info["health"] <= 0 or info["health"] == 0:
        await ctx.send(f"{author.mention} You cannot fight with 0 HP.")
        return
    if info["selected_enemy"] == "None":
        #monster randomising depends on location
        elocation = info["location"]
        if elocation == "Ruins":
            
            monster = ["Froggit", "Whimsun", "Loox", "Vegatoid", "Migosp"]
        if elocation == "Snowdin":
            monster = ["Snowdrake", "Ice Cap", "Gyftrot", "Doggo", "The Lesser Dog", "The Greater Dog"]
        if elocation == "Water Fall":
            monster = ["Aron", "Woshua", "Shyren"]
            
        if elocation == "Hot Land":
            monster = ["Vulkin", "Tsunderplane", "Pyrope"]
            
        if elocation == "Core":
            monster = ["Madjick", "Knight Knight", "Whimsalot", "Final Froggit" , "Astigmatism"]
        if elocation == "last corridor":
           await  ctx.send("But Nobody Came, u?fboss")
           return
        if elocation == "The barrier":
            await ctx.send("But Nobody Came, u?fboss")
            return
        if elocation == "Nothing":
            await ctx.send("Greetings =), u?fboss")
            return
        monsterz = random.choice((monster))
        enemy = monsterz
        monster_hp_min = einfo["locations"][elocation]["enemies"][enemy]["min_health"]
        monster_hp_max = einfo["locations"][elocation]["enemies"][enemy]["max_health"]
        monster_disc = einfo["locations"][elocation]["enemies"][enemy]["dg"]
        ehp_min = monster_hp_min
        ehp_max = monster_hp_max
        enemy_hp = random.randint(ehp_min, ehp_max)
        em_health = info["health"]
        
        if enemy == "Froggit":
        
          frogem = discord.Embed(title="Froggit hopped in!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Froggit's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795500189108011008/image0.png")
          await ctx.send(embed=frogem)
          
        elif enemy == "Whimsun":
          
          wimem = discord.Embed(title="Wimsun came by mistake!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          wimem.set_author(name=f"Fight! Whimsun's HP is {enemy_hp}")
          wimem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795511527733198889/image0.png")
          await ctx.send(embed=wimem)
          
          
          
        elif enemy == "Vegatoid":
          
          vegaemb = discord.Embed(title="Vegatoid Advertise his vegetables", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          vegaemb.set_author(name=f"Fight! Vegatoid's HP is {enemy_hp}")
          vegaemb.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795512555731812362/image0.png")
          await ctx.send(embed=vegaemb)
          
          
          
        elif enemy == "Loox":
          loembd = discord.Embed(title="Loox Drew Near!", description=f"Your HP is {em_health} HP\n\nType **Yes** or **No** in the chat!", color=0x000000)
          loembd.set_author(name=f"Fight! Loox's HP is {enemy_hp}")
          loembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795508978016190474/image0.png")
          await ctx.send(embed=loembd)
          
        elif enemy == "Migosp":
          meembd = discord.Embed(title="Migosp Appeared!", description=f"Your HP is {em_health} HP\n\nType **Yes** or **No** in the chat!", color=0x000000)
          meembd.set_author(name=f"Fight! Migosp HP is {enemy_hp}")
          meembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795539378445221888/image0.png")
          await ctx.send(embed=meembd)
          
        elif enemy == "Snowdrake":
          snowembd = discord.Embed(title="SnowDrake Jumped into here to tell a pun!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          snowembd.set_author(name=f"Fight! Snowdrake's HP is {enemy_hp}")
          snowembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795584864283394048/image0.png")
          await ctx.send(embed=snowembd)
          
        elif enemy == "Ice Cap":
          iceembd = discord.Embed(title="Ice Cap Feeling ignored!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          iceembd.set_author(name=f"Fight! Ice Cap's HP is {enemy_hp}")
          iceembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795725885809623080/image1.png")
          await ctx.send(embed=iceembd)
          
        elif enemy == "Gyftrot":
          gyembd = discord.Embed(title="Gyftrot is undecorating his self!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          gyembd.set_author(name=f"Fight! Gyftrot's HP is {enemy_hp}")
          gyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795728160322879508/image0.png")
          await ctx.send(embed=gyembd)
            
        elif enemy == "Doggo":
          gyembd = discord.Embed(title="Doggo is checking your movement!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          gyembd.set_author(name=f"Fight! Doggo's HP is {enemy_hp}")
          gyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/796804506162954280/image0.png")
          await ctx.send(embed=gyembd)
            
        elif enemy == "The Lesser Dog":
          gyembd = discord.Embed(title="The Lesser Dog Appeared!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          gyembd.set_author(name=f"Fight! The Lesser Dog's HP is {enemy_hp}")
          gyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/796804514878717962/image0.png")
          await ctx.send(embed=gyembd)
            
            
        elif enemy == "The Greater Dog":
          gyembd = discord.Embed(title="The Greater Dog Blocks the way!", description=f"Your HP is {em_health}!\n\nType **Yes** or **No** in the chat!", color=0x000000)
          gyembd.set_author(name=f"Fight! The Greater Dog's HP is {enemy_hp}")
          gyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/796804491658657893/image0.png")
          await ctx.send(embed=gyembd)
          
        elif enemy == "Aron":
          arembd = discord.Embed(title="Aron Flexed throu the battle!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          arembd.set_author(name=f"Fight! Aron's HP is {enemy_hp}")
          arembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795739467896979466/image0.png")
          await ctx.send(embed=arembd)
      

        elif enemy == "Woshua":
          wouembd = discord.Embed(title="Wousha Waches the battle!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          wouembd.set_author(name=f"Fight! Wousha's HP is {enemy_hp}")
          wouembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795739808507887622/image0.png")
          await ctx.send(embed=wouembd)

        elif enemy == "Shyren":
          shyembd = discord.Embed(title="Shyren sings into the battle!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Shyren's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/795740154764984370/image0.webp")
          await ctx.send(embed=shyembd)
            
        elif enemy == "Vulkin":
          shyembd = discord.Embed(title="Vulkin Heats the battle!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Vulkin's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797138389114552320/image0.png")
          await ctx.send(embed=shyembd)
            
            
        elif enemy == "Tsunderplane":
          shyembd = discord.Embed(title="Tsunderplane Flies Throu the battle!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Tsunderplane's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797138406747406416/image0.png")
          await ctx.send(embed=shyembd)
            
        elif enemy == "Pyrope":
          shyembd = discord.Embed(title="Pyrope Waveing the surroundings!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Pyrope's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797138423285547068/image0.png")
          await ctx.send(embed=shyembd)
            
           
        elif enemy == "Madjick":
          wouembd = discord.Embed(title="Madjick Is Here!?!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          wouembd.set_author(name=f"Fight! Madjick's HP is {enemy_hp}")
          wouembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797337093025955880/image0.png")
          await ctx.send(embed=wouembd)

        elif enemy == "Knight Knight":
          shyembd = discord.Embed(title="Knight Knight Protects its place!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Knight Knight's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797337055969542145/image0.png")
          await ctx.send(embed=shyembd)
            
        elif enemy == "Whimsalot":
          shyembd = discord.Embed(title="Whimsalot defends!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Whimsalot's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797337028030365716/image0.png")
          await ctx.send(embed=shyembd)
            
            
        elif enemy == "Final Froggit":
          shyembd = discord.Embed(title="Final Froggit Hopped in!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Final Froggit's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797337036977209344/image0.png")
          await ctx.send(embed=shyembd)
            
        elif enemy == "Astigmatism":
          shyembd = discord.Embed(title="Astigmatism Appeared!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          shyembd.set_author(name=f"Fight! Astigmatism's HP is {enemy_hp}")
          shyembd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/797337046510600232/image0.png")
          await ctx.send(embed=shyembd)
          
        def pred2(m):
            return m.author == message.author and m.channel == message.channel
        answer1 = await bot.wait_for("message", check=pred2, timeout=30)
        values = ["y", "Y", "yes", "Yes", "n", "N", "no", "No", "{}fight".format(Prefix)]
        if str(answer1.content) in values:
            if answer1.content == "{}fight".format(Prefix):
                return
            if answer1.content == "y" or answer1.content == "Y" or answer1.content == "yes" or answer1.content == "Yes":
                info["selected_enemy"] = enemy
                info["enemyhp"] = enemy_hp
                info["in_fight"] = 1
                fileIO("players/{}/info.json".format(author.id), "save", info)
                bot.loop.create_task(fight_loop(ctx))
            elif answer1.content == "n" or answer1.content == "N" or answer1.content == "no" or answer1.content == "No":
                await ctx.send("You flee'd!")
        else:
            await ctx.send("Please choose one of the options next time.")
    else:
      print(f"Beware, Someone is in a fight!, {ctx.author.name}")
      bot.loop.create_task(fight_loop(ctx))
    
    
    #boss fight!
    
@bot.command()
async def fboss(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    message = ctx.message
    await _create_user(author)
    check = fileIO("config/config.json", "load")
    info = fileIO("players/{}/info.json".format(author.id), "load")
    binfo = fileIO("core/enemies/bosses.json", "load")
    curr_time = time.time()
    delta = float(curr_time) - float(info["rest_block"])
    
    
    if delta <= 3600.0 and delta>0:
        seconds = 3600 - delta
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        em = discord.Embed(description="You can't Fight A boss yet!\n\n- Time left:\n **{} Hours, {} Minutes, and {} Seconds**".format(int(h), int(m), int(s)), color=discord.Color.red())
        await ctx.send(embed=em)
        return
    if info["in_fight"] == 1:
        await ctx.send("You are already in a fight!")
        return
    if info["race"] and info["class"] == "None":
        await ctx.send(f"{author.mention} please start your character using u?start")
        return
    if info["health"] <= 0 or info["health"] == 0:
        await ctx.send(f"{author.mention} You cannot fight with 0 HP.")
        return
    if info["selected_enemy"] == "None":
        elocation = info["location"]
        if elocation == "Ruins":
            monster = ["Toriel"]
        if elocation == "Snowdin":
            monster = ["Dogi", "Papyrus"]
        if elocation == "Water Fall":
            monster = ["Dummy", "Undyne"]
        if elocation == "Hot Land":
            monster = ["Royal Guards", "Muffet"]
        if elocation == "Core":
            monster = ["MettatonEX"]
        if elocation == "last corridor":
            monster = ["Sans"]
        if elocation == "The barrier":
            monster = ["Asgore"]
        if elocation == "Nothing":
            monster = ["Chara"]
        
            
        monsterz = random.choice((monster))
        enemy = monsterz
        monster_hp_min = binfo["locations"][elocation]["enemies"][enemy]["min_health"]
        monster_hp_max = binfo["locations"][elocation]["enemies"][enemy]["max_health"]
        ehp_min = monster_hp_min
        ehp_max = monster_hp_max
        enemy_hp = random.randint(ehp_min, ehp_max)
        em_health = info["health"]
        #embed field
        
        if enemy == "Toriel":
        
          frogem = discord.Embed(title="Toriel Blocks The way!!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Toriel's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798619878470058024/image0.png")
          await ctx.send(embed=frogem)
        
        if enemy == "Dogi":
        
          frogem = discord.Embed(title="Couple of dogs Blocks the way!!!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Dogi's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798627314878644294/image0.png")
          await ctx.send(embed=frogem)
        
        if enemy == "Papyrus":
        
          frogem = discord.Embed(title="Nhey heh heeeh!!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Papyrus's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798620238748057600/image0.png")
          await ctx.send(embed=frogem)
        
        if enemy == "Undyne":
        
          frogem = discord.Embed(title="Le Undyne Blocks Da way with determination!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Undyne's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798628314654179378/image0.png")
          await ctx.send(embed=frogem)
        
        
        if enemy == "Dummy":
        
          frogem = discord.Embed(title="The mad Dummy is coming!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Mad Dummy's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798630745291358250/image0.png")
          await ctx.send(embed=frogem)
        
        
        if enemy == "Royal Guards":
        
          frogem = discord.Embed(title="R1 and R2 are here!!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Royal Guards's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798632307581124678/image0.png")
          await ctx.send(embed=frogem)
        
        
        if enemy == "Muffet":
        
          frogem = discord.Embed(title="Muffet is offering some tea ;)!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Muffet's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798621124690444308/image0.png")
          await ctx.send(embed=frogem)
        
        
        if enemy == "MettatonEX":
        
          frogem = discord.Embed(title="Oh Yeaaa!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! MettatonEX's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/798633162581737532/image0.webp")
          await ctx.send(embed=frogem)
        
        if enemy == "Asgore":
        
          frogem = discord.Embed(title="...", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Asgore's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/807461218469281842/image0.webp")
          await ctx.send(embed=frogem)
        
        if enemy == "Sans":
        
          frogem = discord.Embed(title="Its Bad Time Now...", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Sans's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/807461559386767370/image0.png")
          await ctx.send(embed=frogem)
        
        if enemy == "Chara":
        
          frogem = discord.Embed(title="The first fallen human came!", description=f"Your HP is {em_health}\n\nType **Yes** or **No** in the chat!", color=0x000000)
          frogem.set_author(name=f"Fight! Chara's HP is {enemy_hp}")
          frogem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/807461612654034984/image0.jpg")
          await ctx.send(embed=frogem)
        
        #proceed!
        def pred2(m):
            return m.author == message.author and m.channel == message.channel
        answer1 = await bot.wait_for("message", check=pred2, timeout=30)
        values = ["y", "Y", "yes", "Yes", "n", "N", "no", "No", "{}fight".format(Prefix)]
        if str(answer1.content) in values:
            if answer1.content == "{}fight".format(Prefix):
                return
            if answer1.content == "y" or answer1.content == "Y" or answer1.content == "yes" or answer1.content == "Yes":
                info["selected_enemy"] = enemy
                info["enemyhp"] = enemy_hp
                info["in_fight"] = 1
                info["rest_block"] = curr_time
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await boss_loop(ctx)
            elif answer1.content == "n" or answer1.content == "N" or answer1.content == "no" or answer1.content == "No":
                await ctx.send("You Ran Away!")
        else:
            await ctx.send("Please choose one of the options next time.")
    else:
      await boss_loop(ctx)
   


async def spare(ctx):
  author = ctx.author
  info = fileIO("players/{}/info.json".format(author.id), "load")
  info = fileIO("players/{}/info.json".format(author.id), "load")
  monster = info["selected_enemy"]
  if info["selected_enemy"] == "Sans":
    await ctx.send("Get dunked on!!, if were really freinds... **YOU WON'T COME BACK**")
    return

  else:
    func = ["spared", "NotSpared", "spared"]
    sprfunc = random.choice((func))
    embed1 = Embed(title='Mercy', description=f"You tried to spare *{monster}*")
    embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803887253927100436/image0.png")
    msg = await ctx.send(embed=embed1)
    await asyncio.sleep(5)
    embed2 = Embed(title='Mercy', description=f"They didn't accepted your mercy")
    embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803889297936613416/image0.png")
    embed3 = Embed(title='Mercy', description=f"They accepted your mercy")
    embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803887253927100436/image0.png")
    if sprfunc == "spared":
      info["selected_enemy"] = "None"
      info["in_fight"] = 0
      await msg.edit(embed=embed3)
      fileIO("players/{}/info.json".format(author.id), "save", info)
    elif sprfunc == "NotSpared":
      await msg.edit(embed=embed2)
      info["health"] = info["health"] - 6
      fileIO("players/{}/info.json".format(author.id), "save", info)
      await asyncio.sleep(7)
      bot.loop.create_task(fight_loop(ctx))
    else:
      await ctx.reply("error!")
    
    
async def spare_boss(ctx):
  author = ctx.author
  info = fileIO("players/{}/info.json".format(author.id), "load")
  monster = info["selected_enemy"]
  if info["selected_enemy"] == "Sans":
    await ctx.send("Get dunked on!!, if were really freinds... **YOU WON'T COME BACK**")
    return

  else:
    func = ["spared", "NotSpared", "spared"]
    sprfunc = random.choice((func))
    embed1 = Embed(title='Mercy', description=f"You tried to spare *{monster}*")
    embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803887253927100436/image0.png")
    msg = await ctx.send(embed=embed1)
    await asyncio.sleep(5)
    embed2 = Embed(title='Mercy', description=f"They didn't accepted your mercy")
    embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803889297936613416/image0.png")
    embed3 = Embed(title='Mercy', description=f"They accepted your mercy")
    embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803887253927100436/image0.png")
    if sprfunc == "spared":
      info["selected_enemy"] = "None"
      info["in_fight"] = 0
      await msg.edit(embed=embed3)
      fileIO("players/{}/info.json".format(author.id), "save", info)
    elif sprfunc == "NotSpared":
      await msg.edit(embed=embed2)
      info["health"] = info["health"] - 6
      fileIO("players/{}/info.json".format(author.id), "save", info)
      await asyncio.sleep(7)
      bot.loop.create_task(boss_loop(ctx))
    else:
      await ctx.reply("error!")
#######################
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def equip(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    await _create_user(author)
    message = ctx.message
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        await ctx.send("Please start your character using `{}start`".format(Prefix))
        return
    choices = []
    inv_list = [i for i in info["inventory"]]
    if len(inv_list) == 0:
        em = discord.Embed(description="```diff\n- You don't have anything else to equip!```", color=discord.Color.red())
        await ctx.send(embed=em)
    else:
        choices.append(inv_list)
        em = discord.Embed(description="```diff\n+ What would you like to equip?\n\n- Note this is Uppercase and Lowercase sensitive.\n\n{}```".format("\n\n".join(inv_list)), color=discord.Color.blue())
        await ctx.send(embed=em)
        def pred3(m):
            return m.author == message.author and m.channel == message.channel
        answer1 = await bot.wait_for("message", check=pred3, timeout=30)
        if answer1.content in inv_list:
            em = discord.Embed(description="```diff\n+ You equip the {}!```".format(answer1.content), color=discord.Color.blue())
            await ctx.send(embed=em)
            info["inventory"].append(info["equip"])
            info["equip"] = "None"
            info["equip"] = answer1.content
            info["inventory"].remove(answer1.content)
            fileIO("players/{}/info.json".format(author.id), "save", info)
        else:
            await ctx.send("<@{}> please choose a valid item next time.".format(author.id))
            
            
     
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.cooldown(1, 7, commands.BucketType.user)
async def armor(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    await _create_user(author)
    message = ctx.message
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        await ctx.send("Please start your character using `{}start`".format(Prefix))
        return
    choices = []
    inv_list = [i for i in info["inv_armor"]]
    if len(inv_list) == 0:
        em = discord.Embed(description="```diff\n- You don't have anything else to equip!```", color=discord.Color.red())
        await ctx.send(embed=em)
    else:
        choices.append(inv_list)
        em = discord.Embed(description="```diff\n+ What would you like to equip?\n\n\n- Note this is Uppercase and Lowercase sensitive.\n\n{}```".format("\n\n".join(inv_list)), color=discord.Color.blue())
        await ctx.send(embed=em)
        def pred3(m):
            return m.author == message.author and m.channel == message.channel
        answer1 = await bot.wait_for("message", check=pred3, timeout=30)
        if answer1.content in inv_list:
            em = discord.Embed(description="```diff\n+ You equip the {}!```".format(answer1.content), color=discord.Color.blue())
            await ctx.send(embed=em)
            info["inv_armor"].append(info["wearing"])
            info["wearing"] = "None"
            info["wearing"] = answer1.content
            info["inv_armor"].remove(answer1.content)
            fileIO("players/{}/info.json".format(author.id), "save", info)
        else:
            await ctx.send("<@{}> please choose a valid item next time.".format(author.id))
           
 ###############################
################################
################################
 
       

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.cooldown(1, 8, commands.BucketType.user)
async def lootbag(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    channel = ctx.channel
    author = ctx.author
    await _create_user(author)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        await ctx.send("Please start your character using `{}start`".format(Prefix))
        return
    if info["in_fight"] == 1:
        return
    if info["lootbag"] == 0:
        em = discord.Embed(description="**You dont have any lootbags!**", color=discord.Color.blue())
        await ctx.send(embed=em)
        return
    else:
        em = discord.Embed(description="```diff\n+ {} Starts opening a Lootbag. . .```".format(info["name"]), color=discord.Color.blue())
        await ctx.send(embed=em)
        await asyncio.sleep(5)
        chance = random.randint(1, 3)
        goldmul = random.randint(10, 30)
        goldgain = goldmul + info["lvl"]
        em = discord.Embed(description="```diff\n+ The Lootbag obtained {} Gold!```".format(goldgain), color=discord.Color.blue())
        await ctx.send(embed=em)
        info["gold"] = info["gold"] + goldgain
        info["lootbag"] = info["lootbag"] - 1
        fileIO("players/{}/info.json".format(author.id), "save", info)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.cooldown(1, 8, commands.BucketType.user)
async def travel(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    channel = ctx.channel
    author = ctx.author
    message = ctx.message
    await _create_user(author)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        await ctx.send("Please start your character using `{}start`".format(Prefix))
        return
    if info["selected_enemy"] != "None":
      await ctx.send("You cannot travel while fighting, try to ?spare!")
      return
    options = []
    options2 = []
    travel_location = []
    #level 1
    if info["lvl"] > 0 and info["lvl"] < 3:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(LV.3) Showdin")
        options.append("(LV.10) WaterFall")
        options.append("(LV.15) HotLand")
        options.append("(LV.20) Core")
        options.append("(LV.50) The barrier")
        options.append("(LV.60) last corridor")
        options.append("(LV.99) Void")
    #level 3
    if info["lvl"] >= 3 and info["lvl"] < 10:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(LV.10) WaterFall")
        options.append("(LV.15) HotLand")
        options.append("(LV.20) Core")
        options.append("(LV.50) The barrier")
        options.append("(LV.60) last corridor")
        options.append("(LV.99) Void")

    if info["lvl"] >= 10 and info["lvl"] < 15:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(2) WaterFall")
        options2.append("2")
        options.append("(LV.15) HotLand")
        options.append("(LV.20) Core")
        options.append("(LV.50) The barrier")
        options.append("(LV.60) last corridor")
        options.append("(LV.99) Void")
        
    if info["lvl"] >= 15 and info["lvl"] < 20:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(2) WaterFall")
        options2.append("2")
        options.append("(3) Hot Land")
        options2.append("3")
        options.append("(LV.20) Core")
        options.append("(LV.50) The barrier")
        options.append("(LV.60) last corridor")
        options.append("(LV.99) Void")
     
    if info["lvl"] >= 20 and info["lvl"] < 50:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(2) WaterFall")
        options2.append("2")
        options.append("(3) Hot Land")
        options2.append("3")
        options.append("(4) Core")
        options2.append("4")
        options.append("(LV.50) The barrier")
        options.append("(LV.60) last corridor")
        options.append("(LV.99) Void")
    if info["lvl"] >= 50 and info["lvl"] < 60:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(2) WaterFall")
        options2.append("2")
        options.append("(3) Hot Land")
        options2.append("3")
        options.append("(4) Core")
        options2.append("4")
        options.append("(5) The barrier")
        options2.append("5")
        options.append("(LV.60) last corridor")
        options.append("(LV.99) Void")
    
    
    if info["lvl"] >= 60 and info["lvl"] < 99:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(2) WaterFall")
        options2.append("2")
        options.append("(3) Hot Land")
        options2.append("3")
        options.append("(4) Core")
        options2.append("4")
        options.append("(5) The barrier")
        options2.append("5")
        options.append("(6) last corridor")
        options2.append("6")
        options.append("(LV.99) Void")
    
    if info["lvl"] == 99:
        options.append("(0) Ruins")
        options2.append("0")
        options.append("(1) Snowdin")
        options2.append("1")
        options.append("(2) WaterFall")
        options2.append("2")
        options.append("(3) Hot Land")
        options2.append("3")
        options.append("(4) Core")
        options2.append("4")
        options.append("(5) The barrier")
        options2.append("5")
        options.append("(6) last corridor")
        options2.append("6")
        options.append("(7) =)")
        options2.append("7")

    em = discord.Embed(description="<@{}>\n```diff\n+ Where would you like to travel?\n- Type a location number in the chat.\n+ {}```".format(author.id, "\n\n+ ".join(options)), color=discord.Color.blue())
    await ctx.send(embed=em)

    def pred4(m):
        return m.author == message.author and m.channel == message.channel
    answer1 = await bot.wait_for("message", check=pred4, timeout=30)

    if answer1.content in options2:
        if answer1.content == "0":
            if info["location"] == "Ruins":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "Ruins"
                info["location"] = "Ruins"
                info["selected_enemy"] = "None"

        elif answer1.content == "1":
            if info["location"] == "Snowdin":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "Snowdin"
                info["location"] = "Snowdin"
                info["selected_enemy"] = "None"

        elif answer1.content == "2":
            if info["location"] == "Water Fall":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "Water Fall"
                info["location"] = "Water Fall"
                info["selected_enemy"] = "None"
            
        elif answer1.content == "3":
            if info["location"] == "Hot Land":
                em = discord.Embed(description=f"{author.name}\n\nYou're already at HotLand!", color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "Hot Land"
                info["location"] = "Hot Land"
                info["selected_enemy"] = "None"
        
        elif answer1.content == "4":
            if info["location"] == "Core":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "Core"
                info["location"] = "Core"
                info["selected_enemy"] = "None"
                
        if answer1.content == "5":
            if info["location"] == "The barrier":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "The barrier"
                info["location"] = "The barrier"
                info["selected_enemy"] = "None"
                
        if answer1.content == "6":
            if info["location"] == "last corridor":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "last corridor"
                info["location"] = "last corridor"
                info["selected_enemy"] = "None"
                
        if answer1.content == "7":
            if info["location"] == "Nothing":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(author.id, info["location"]), color=discord.Color.red())
                await ctx.send(embed=em)
                return
            else:
                location_name = "Nothing"
                info["location"] = "Nothing"
                info["selected_enemy"] = "None"

        em = discord.Embed(description=f"{author.name} Traveling to {location_name}...", color=discord.Color.red())
        await ctx.send(embed=em)
        await asyncio.sleep(3)
        info["location"] = location_name
        fileIO("players/{}/info.json".format(author.id), "save", info)
        em = discord.Embed(description=f"{author.name}\n\nYou have arrived at {location_name}")
        await ctx.send(embed=em)
    else:
        await ctx.send("Please choose a correct location next time.")
        
        
        
        ############ SHOP1 #############
#######################################################

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.cooldown(1, 12, commands.BucketType.user)
async def shop(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    await _create_user(author)
    message = ctx.message
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["selected_enemy"] != "None":
      await ctx.send("You cant open shop while fighting!, Try ?spare")
      return
    em = discord.Embed(description="What category would you like to buy from?\n- **Potions**\n- **items**", color=discord.Color.blue())
    await ctx.send(embed=em)
    options = ["potions", "Potions", "items", "Items", "{}buy".format(Prefix)]
    def pred5(m):
        return m.author == message.author and m.channel == message.channel
    answer1 = await bot.wait_for("message", check=pred5, timeout=30)
    if answer1.content in options:
        if answer1.content == "{}buy".format(Prefix):
            return
        elif answer1.content == "potions" or answer1.content == "Potions":
            if info["hp_potions"] >= info["max_pot"]:
                info["hp_potions"] = info["max_pot"]
                await ctx.send("You can't buy more than 6 potions!")
                return
            em = discord.Embed(description="How many would you like to buy?\n\neach for **30G**.", color=discord.Color.blue())
            await ctx.send(embed=em)
            def pred6(m):
                return m.author == message.author and m.channel == message.channel
            answer2 = await bot.wait_for("message", check=pred6, timeout=30)
            try:
                value = int(answer2.content) * 30
                if info["gold"] < value:
                    em = discord.Embed(description="{}, seems like you don't have the enough money!".format(info["name"], answer2.content), color=discord.Color.red())
                    await ctx.send(embed=em)
                else:
                    info["gold"] = info["gold"] - value
                    info["hp_potions"] = info["hp_potions"] + int(answer2.content)
                    fileIO("players/{}/info.json".format(author.id), "save", info)
                    em = discord.Embed(description="{}, you bought {} potion(s) for **{}G**".format(info["name"], answer2.content, value), color=discord.Color.blue())
                    await ctx.send(embed=em)
            except:
                em = discord.Embed(description="{}, That is not a number isn't it?".format(info["name"]), color=discord.Color.red())
                await ctx.send(embed=em)
                
        elif answer1.content == "items" or answer1.content == "Items":
          #Ruins Shop
          if info["location"] == "Ruins":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Toy Knife** | **1200G**")
            await ctx.send(embed=shoem)
            def pred7(m):
                 return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred7, timeout=30)
            if answer3.content == "Toy Knife" or answer3.content == "toy knife":
              if info["gold"] < int(1200):
                await ctx.send("you cant afford that!")
              else:
                info["gold"] = info["gold"] - 1200
                info["inventory"].append("Toy Knife")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("You Successfully purchased The **Toy Knife**")
            else:
                await ctx.send("That is'nt availble here, tho?")
          elif info["location"] == "Snowdin":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Tough Gloves** | **3200G**")
            await ctx.send(embed=shoem)
            def pred8(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred8, timeout=30)
            if answer3.content == "Tough Gloves" or answer3.content == "tough gloves":
              if info["gold"] < 3200:
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 3200
                info["inventory"].append("Tough Gloves")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Tough Gloves!")
            else:
                await ctx.send("Invalid Item!")
                
          
          elif info["location"] == "Water Fall":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Ballet Shoes** | **4800G**\n\n**Torn Notebook** | **2200G**")
            await ctx.send(embed=shoem)
            def pred9(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred9, timeout=30)
            if answer3.content == "Ballet Shoes" or answer3.content == "ballet shoes":
              if info["gold"] < int(4800):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 4800
                info["inventory"].append("Ballet Shoes")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Ballet Shoes!")
                
            elif answer3.content == "Torn Notebook" or answer3.content == "torn notebook":
              if info["gold"] < int(2200):
                 await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 2200
                info["inventory"].append("Torn Notebook")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Torn Notebook!")
            
          elif info["location"] == "Hot Land":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Burnt Pan** | **6600G**")
            await ctx.send(embed=shoem)
            def pred10(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred10, timeout=30)
            if answer3.content == "Burnt Pan" or answer3.content == "burnt pan":
              if info["gold"] < int(6600):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 6600
                info["inventory"].append("Burnt Pan")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Burnt Pan!")
        
          elif info["location"] == "Core":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Empty Gun** | **8400G**")
            await ctx.send(embed=shoem)
            def pred11(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred11, timeout=30)
            if answer3.content == "Empty Gun" or answer3.content == "empty gun":
              if info["gold"] < int(8400):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 8400
                info["inventory"].append("Empty Gun")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Burnt Pan!")
                
          elif info["location"] == "The barrier":
                shoem = discord.Embed(description="Here is the availble Items!\n\n**Worn Dagger** | **10200**")
                await ctx.send(embed=shoem)
                def pred11(m):
                      return m.author == message.author and m.channel == message.channel
                answer3 = await bot.wait_for("message", check=pred11, timeout=30)
                if answer3.content == "Worn Dagger" or answer3.content == "worn dagger":
                  if info["gold"] < int(10200):
                   await ctx.send("You can't afford that!")
                  else:
                    info["gold"] = info["gold"] - 10200
                    info["inventory"].append("Worn Dagger")
                    fileIO("players/{}/info.json".format(author.id), "save", info)
                    await ctx.send("Successfully purchased Worn Dagger!")
                
                
          elif info["location"] == "last corridor":
                shoem = discord.Embed(description="Here is the availble Items!\n\n**Real Knife** | **20000G**")
                await ctx.send(embed=shoem)
                def pred11(m):
                      return m.author == message.author and m.channel == message.channel
                answer3 = await bot.wait_for("message", check=pred11, timeout=30)
                if answer3.content == "Real Knife" or answer3.content == "real knife":
                  if info["gold"] < int(20000):
                   await ctx.send("You can't afford that!")
                  else:
                    info["gold"] = info["gold"] - 20000
                    info["inventory"].append("Real Knife")
                    fileIO("players/{}/info.json".format(author.id), "save", info)
                    await ctx.send("Successfully purchased Real Knife!")
                  
                else:
                    await ctx.send("Invalid Item!")
                        
        else:
            em = discord.Embed(description="{} ,We don't have such category named that name!".format(info["name"]), color=discord.Color.red())
            await ctx.send(embed=em)
    else:
        em = discord.Embed(description="```diff\n- {}, please put a correct value next time.```".format(info["name"]), color=discord.Color.red())
        await ctx.send(embed=em)
        
        ######    SHOP 2   #######
#######################################
        
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.cooldown(1, 12, commands.BucketType.user)
async def arshop(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    await _create_user(author)
    message = ctx.message
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["in_fight"] == 1:
      await ctx.send("You cant open shop while fighting!.")
          #Ruins Shop
        
        
    if info["location"] == "Ruins":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Faded Ribbon** | **700G**")
            await ctx.send(embed=shoem)
            def pred7(m):
                 return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred7, timeout=30)
            if answer3.content == "Faded Ribbon" or answer3.content == "faded ribbon":
              if info["gold"] < int(700):
                await ctx.send("you cant afford that!")
              else:
                info["gold"] = info["gold"] - 700
                info["inv_armor"].append("Faded Ribbon")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("You Successfully purchased The **Faded Ribbon**")
            else:
                await ctx.send("That isn't availble here, tho?")
    
    
    elif info["location"] == "Snowdin":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Manly Bandanna** | **1400G**")
            await ctx.send(embed=shoem)
            def pred8(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred8, timeout=30)
            if answer3.content == "Manly Bandanna" or answer3.content == "manly bandanna":
              if info["gold"] < 1400:
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 1400
                info["inv_armor"].append("Manly Bandanna")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Manly Bandanna!")
            else:
                await ctx.send("Invalid Item!")
                
        
    elif info["location"] == "Water Fall":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Old Tutu** | **1900G**\n\n**Cloudy Glasses** | **1700G**")
            await ctx.send(embed=shoem)
            def pred9(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred9, timeout=30)
            if answer3.content == "Old Tutu" or answer3.content == "old tutu":
              if info["gold"] < int(1900):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 1900
                info["inv_armor"].append("Old Tutu")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Ballet Shoes!")
                
            elif answer3.content == "Cloudy Glasses" or answer3.content == "cloudy glasses":
              if info["gold"] < int(1700):
                 await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 1700
                info["inv_armor"].append("Cloudy Glasses")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Cloudy Glasses!")
            
            
            
    elif info["location"] == "Hot Land":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Stained Arpon** | **G2500**")
            await ctx.send(embed=shoem)
            def pred10(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred10, timeout=30)
            if answer3.content == "Stained Arpon" or answer3.content == "stained arpon":
              if info["gold"] < int(2500):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 2500
                info["inv_armor"].append("Stained Arpon")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Stained Arpon!")
        
        
        
    elif info["location"] == "Core":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Cowboy Hat** | **3400G**")
            await ctx.send(embed=shoem)
            def pred11(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred11, timeout=30)
            if answer3.content == "Cowboy Hat" or answer3.content == "cowboy hat":
              if info["gold"] < int(3400):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 3400
                info["inv_armor"].append("Cowboy Hat")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Cowboy Hat!")
                
            else:
                await ctx.send("Invalid Item!")
                
              
    elif info["location"] == "The barrier":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**Heart Locked** | **7200G**")
            await ctx.send(embed=shoem)
            def pred11(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred11, timeout=30)
            if answer3.content == "Heart Locket" or answer3.content == "heart locket":
              if info["gold"] < int(7200):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 7200
                info["inv_armor"].append("Heart Locket")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased Heart Locket!")
                
            else:
                await ctx.send("Invalid Item!")
                
    elif info["location"] == "last corridor":
            shoem = discord.Embed(description="Here is the availble Items!\n\n**The Locket** | **10000G**")
            await ctx.send(embed=shoem)
            def pred11(m):
                  return m.author == message.author and m.channel == message.channel
            answer3 = await bot.wait_for("message", check=pred11, timeout=30)
            if answer3.content == "The Locket" or answer3.content == "the locket":
              if info["gold"] < int(10000):
               await ctx.send("You can't afford that!")
              else:
                info["gold"] = info["gold"] - 10000
                info["inv_armor"].append("The Locket")
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.send("Successfully purchased The Locket!")
                
            else:
                await ctx.send("Invalid Item!")
            
      

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
@commands.cooldown(1, 12, commands.BucketType.user)
async def heal(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    author = ctx.author
    await _create_user(author)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        await ctx.send("Please start your character using `{}start`".format(Prefix))
        return
    if info["hp_potions"] > 0:
      if info["health"] >= info["max_health"]:
        await ctx.send("your health is maxed!")
        return
      gain = random.randint(90, 100)                
      info["health"] = info["health"] + gain
      if info["health"] > info["max_health"]:
          info["health"] = info["max_health"]
      info["hp_potions"] = info["hp_potions"] - 1
      fileIO("players/{}/info.json".format(author.id), "save", info)
      em = discord.Embed(description="```diff\n- You use a Minor Health Potion\n+ {} HP```".format(gain), color=discord.Color.blue())
      await ctx.send(embed=em)
    else:
        em = discord.Embed(description="```diff\n- You don't have any health    potions!```", color=discord.Color.red())
        await ctx.send(embed=em)
        
        
@bot.command()
@commands.cooldown(1, 12, commands.BucketType.user)
async def daily(ctx):
    check = fileIO("config/config.json", "load")
    if check["Global"] == "Disabled":
        await ctx.send("Command is Globaly Down for maintainance, Try again Later!")
        return
    channel = ctx.channel
    author = ctx.author
    await _create_user(author)
    goldget = random.randint(500, 1000)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] and info["class"] == "None":
        await ctx.send("Please start your character using `{}start`".format(Prefix))
        return
    curr_time = time.time()
    delta = float(curr_time) - float(info["daily_block"])

    if delta >= 86400.0 and delta>0:
        if info["class"] == "None" and info["race"] == "None":
            await ctx.send("Please start your player using `{}start`".format(Prefix))
            return
        info["gold"] += goldget
        info["daily_block"] = curr_time
        fileIO("players/{}/info.json".format(author.id), "save", info)
        em = discord.Embed(description="```diff\n+ You recieved your daily gold!\n+ {}```".format(goldget), color=discord.Color.blue())
        await ctx.send(embed=em)
    else:
        seconds = 86400 - delta
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        em = discord.Embed(description="You can't claim your daily reward yet!\n\n- Time left:\n **{} Hours, {} Minutes, and {} Seconds**".format(int(h), int(m), int(s)), color=discord.Color.red())
        await ctx.send(embed=em)
   
    
@bot.command()
async def debug(ctx):
    author = ctx.author
    info = fileIO("players/{}/info.json".format(author.id), "load")
    info["in_fight"] = 0
    fileIO("players/{}/info.json".format(author.id), "save", info)
    await ctx.reply("reseted")
  
async def heal_loop(ctx):
    author = ctx.author
    await _create_user(author)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["hp_potions"] > 0:
      gain = random.randint(90, 100)                
      info["health"] = info["health"] + gain
      if info["health"] > info["max_health"]:
          info["health"] = info["max_health"]
      info["hp_potions"] = info["hp_potions"] - 1
      fileIO("players/{}/info.json".format(author.id), "save", info)
      em = discord.Embed(description="```diff\n- You use a Minor Health Potion\n+ {} HP```".format(gain), color=discord.Color.blue())
      await ctx.send(embed=em)
      await asyncio.sleep(3)
      bot.loop.create_task(fight_loop(ctx))
    else:
        em = discord.Embed(description="```diff\n- You don't have any health    potions!```", color=discord.Color.red())
        await ctx.send(embed=em)
        await asyncio.sleep(6)
        bot.loop.create_task(fight_loop(ctx))
        
        
        
async def heal_boss(ctx):
    author = ctx.author
    await _create_user(author)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["hp_potions"] > 0:
      gain = random.randint(90, 100)                
      info["health"] = info["health"] + gain
      if info["health"] > info["max_health"]:
          info["health"] = info["max_health"]
      info["hp_potions"] = info["hp_potions"] - 1
      fileIO("players/{}/info.json".format(author.id), "save", info)
      em = discord.Embed(description="```diff\n- You use a Minor Health Potion\n+ {} HP```".format(gain), color=discord.Color.blue())
      await ctx.send(embed=em)
      await asyncio.sleep(3)
      bot.loop.create_task(boss_loop(ctx))
    else:
        em = discord.Embed(description="```diff\n- You don't have any health    potions!```", color=discord.Color.red())
        await ctx.send(embed=em)
        await asyncio.sleep(6)
        bot.loop.create_task(boss_loop(ctx))

#--------------------------------------------------------------------------#
#-------------------------------OTHER VALUES-------------------------------#
#--------------------------------------------------------------------------#
async def _check_levelup(ctx):
    author = ctx.author
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["lvl"] >= 99:
        await asyncio.sleep(3)
        await ctx.send("you can make your stats better by u?reset, *coming soon*")
    xp = info["exp"]
    num = 100
    name = info["name"]
    lvl = info["lvl"]
    lvlexp = num * lvl
    if xp >= lvlexp:
        info["lvl"] = info["lvl"] + 1
        info["exp"] = 0
        info["max_health"] = info["max_health"] + 4
        info["damage"] = info["damage"] + 1
        new_lvl = info["lvl"]
        new_dmg = info["damage"]
        fileIO("players/{}/info.json".format(author.id), "save", info)
        await ctx.send(f"{author.mention} Your LOVE increased, your love is **{new_lvl}**, damage increased to {new_dmg}")
        return await _check_levelup(ctx)
    else:
        pass

async def _pick_class(ctx):
    author = ctx.author
    message = ctx.message
    info = fileIO("players/{}/info.json".format(author.id), "load")
    if info["race"] == "Normal":
            info["skills_learned"].append("Shoot")
            info["equip"] = "Stick"
            info["class"] = "Undertale"
            fileIO("players/{}/info.json".format(author.id), "save", info)
            await ctx.send("All setup!")
            return    
    else:
        return
        
#fight loop!
        
        
async def fight_loop(ctx):
  while True:
      author = ctx.author
      message = ctx.message
      info = fileIO("players/{}/info.json".format(author.id), "load")
      einfo = fileIO("core/enemies/enemies.json", "load")
      #Define our user stats here.
      user_location = info["location"]
      user_enemy = info["selected_enemy"]
      user_enemy_hp = info["enemyhp"]
      user_skills = info["skills_learned"]
      user_wep = info["equip"]
      user_ar = info["wearing"]
      user_hp = info["health"]
      user_name = info["name"]
      #Define wep dmg.
      ainfo = fileIO("core/enemies/weapons.json", "load")
      dinfo = fileIO("core/enemies/armor.json", "load")
      user_wep_define = ainfo[user_wep]
      min_dmg = ainfo[user_wep]["min_dmg"]
      min_dfs = dinfo[user_ar]["min_dfs"]
      max_dmg = ainfo[user_wep]["max_dmg"]
      max_dfs = dinfo[user_ar]["max_dfs"]
      user_dmg = random.randint(min_dmg, max_dmg)
      user_dfs = random.randint(min_dfs, max_dfs)
      #Define enemy stats.
      enemy_define = info["selected_enemy"]
      enemy_define_hp = info["enemyhp"]
      enemy_min_dmg = einfo["locations"][user_location]["enemies"][user_enemy]["min_dmg"]
      enemy_max_dmg = einfo["locations"][user_location]["enemies"][user_enemy]["max_dmg"]
      enemy_dmg = random.randint(enemy_min_dmg, enemy_max_dmg) - int(user_dfs)
      enemy_min_gold = einfo["locations"][user_location]["enemies"][user_enemy]["min_drop"]
      enemy_max_gold = einfo["locations"][user_location]["enemies"][user_enemy]["max_drop"]
      enemy_gold = random.randint(enemy_min_gold, enemy_max_gold)
      enemy_xp_min = einfo["locations"][user_location]["enemies"][user_enemy]["min_xp"]
      enemy_xp_max = einfo["locations"][user_location]["enemies"][user_enemy]["max_xp"]
      dg = einfo["locations"][user_location]["enemies"][user_enemy]["dg2"]
      enemy_xp = random.randint(enemy_xp_min, enemy_xp_max)
      if enemy_dmg < 0:
        enemy_dmg = 0
     #Skill Usage
      embd = discord.Embed(description="Choose one of the options and write it in the chat **WITHOUT THE PREFIX!**!\n\n\n\n\n**Fight**                           **Act**                           **Mercy**                   ")
      await ctx.send(embed=embd)
      def pred(m):
        return m.author == message.author and m.channel == message.channel
      try:
        answer1 = await bot.wait_for("message", check=pred, timeout=30)
        
        if answer1.content == "Fight" or answer1.content == "fight":
            #Lootbag# 10% chance to obtain one from an enemy.
              
            lootbag = random.randint(1, 10)
            damage = info["damage"]
            enemy_hp = user_enemy_hp
            
            
            
            #player attack
            enemy_hp_after = int(enemy_hp) - int(user_dmg) - int(damage)
            atem = discord.Embed(title="You Attack", description=f"You Damaged **{enemy_define}**, **-{user_dmg}HP** | current monster hp: **{enemy_hp_after}**", color=0xe74c3c)
            atem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803885802588733460/image0.png")
            await asyncio.sleep(2)
            await ctx.reply(embed=atem)
            if enemy_hp_after < 0:
                enemy_hp_after = 0
                femb=discord.Embed(description=f"You Won, Earned {enemy_gold}G and {enemy_xp}XP", color=0xe74c3c)
                await ctx.reply(embed=femb)
                info["selected_enemy"] = "None"
                info["enemyhp"] = 50
                info["in_fight"] = 0
                info["gold"] = info["gold"] + enemy_gold
                info ["exp"] = info["exp"] + enemy_xp
                if lootbag == 6:
                    await ctx.reply(f"{ctx.author.mention} You got a lootbag, u?lootbag and see your!!")
                    await asyncio.sleep(2)
                    info["lootbag"] = info["lootbag"] + 1
                    fileIO("players/{}/info.json".format(author.id), "save", info)
                info["enemieskilled"] = info["enemieskilled"] + 1
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await _check_levelup(ctx)
                break
                
            else:
                info["enemyhp"] = enemy_hp_after
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await asyncio.sleep(5)
                            
            #monster attack
            user_hp_after = int(user_hp) - int(enemy_dmg)
            gold_lost = random.randint(60, 220)
            atem = discord.Embed(title="Attack!", description=f"**{enemy_define}** Attacks, **-{enemy_dmg}HP** | current hp: **{user_hp_after}**", color=0xe74c3c)
            atem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803885802588733460/image0.png")
            await asyncio.sleep(2)
            await ctx.reply(embed=atem)
            
            
            
            
            if user_hp_after < 0:
                user_hp_after = 0
                info["gold"] = info["gold"] - gold_lost
                if info["gold"] < 0:
                    info["gold"] = 0
                info["deaths"] = info["deaths"] + 1
                info["health"] = 0
                info["in_fight"] = 0
                info["selected_enemy"] = "None"
                info["enemyhp"] = 50
                fileIO("players/{}/info.json".format(author.id), "save", info)
                
                
                femb=discord.Embed(description=f"**You Lost**\n\n**Stay Determines please!, You lost {gold_lost}G**")
                femb.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/804303928929812481/BA305022-ADCB-4DEE-84D5-01C54A1C85CF.gif")
                await asyncio.sleep(2)
                await ctx.reply(embed=femb)
                break
            else:
                info["health"] = user_hp_after
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await asyncio.sleep(5)
                
        elif answer1.content == "Mercy" or answer1.content == "mercy":
          await spare(ctx)
          break
            
        elif answer1.content == "Act" or answer1.content == "act":
            embed=discord.Embed(title="Acts", description="Choose:\n\n**Check\n\nHeal**")
            await ctx.send(embed=embed)
            def pred(m):
                return m.author == message.author and m.channel == message.channel
            try:
                answer1 = await bot.wait_for("message", check=pred, timeout=30)
        
                if answer1.content == "Check" or answer1.content == "check":
                    embch=discord.Embed(title="Monster Stats", description=f"**{enemy_max_dmg}DMG\n\n{dg}**")
                    await ctx.send(embed=embch)
                    await asyncio.sleep(6)
                elif answer1.content == "Heal" or answer1.content == "heal":
                    await heal_loop(ctx)
                    break
                    
                else:
                    await ctx.send("Please choose the corret option!")
                    await asyncio.sleep(6)
                    bot.loop.create_task(fight_loop(ctx))
                    break
                    
            except asyncio.TimeoutError:
                info["in_fight"] = 0
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.reply("You Missed!")
                break
      except asyncio.TimeoutError:
                info["in_fight"] = 0
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await ctx.reply("You Missed!")
                break
          

async def boss_loop(ctx):
  while True:
      author = ctx.author
      message = ctx.message
      info = fileIO("players/{}/info.json".format(author.id), "load")
      einfo = fileIO("core/enemies/bosses.json", "load")
      #Define our user stats here.
      user_location = info["location"]
      user_enemy = info["selected_enemy"]
      user_enemy_hp = info["enemyhp"]
      user_skills = info["skills_learned"]
      user_wep = info["equip"]
      user_ar = info["wearing"]
      user_hp = info["health"]
      user_name = info["name"]
      #Define wep dmg.
      ainfo = fileIO("core/enemies/weapons.json", "load")
      dinfo = fileIO("core/enemies/armor.json", "load")
      user_wep_define = ainfo[user_wep]
      user_ar_define = dinfo[user_ar]
      min_dmg = ainfo[user_wep]["min_dmg"]
      min_dfs = dinfo[user_ar]["min_dfs"]
      max_dmg = ainfo[user_wep]["max_dmg"]
      max_dfs = dinfo[user_ar]["max_dfs"]
      user_dmg = random.randint(min_dmg, max_dmg)
      user_dfs = random.randint(min_dfs, max_dfs)
      #Define enemy stats.
      enemy_define = info["selected_enemy"]
      enemy_define_hp = info["enemyhp"]
      enemy_min_dmg = einfo["locations"][user_location]["enemies"][user_enemy]["min_dmg"]
      enemy_max_dmg = einfo["locations"][user_location]["enemies"][user_enemy]["max_dmg"]
      enemy_dmg = random.randint(enemy_min_dmg, enemy_max_dmg) - int(user_dfs)
      enemy_min_gold = einfo["locations"][user_location]["enemies"][user_enemy]["min_drop"]
      enemy_max_gold = einfo["locations"][user_location]["enemies"][user_enemy]["max_drop"]
      enemy_gold = random.randint(enemy_min_gold, enemy_max_gold)
      enemy_xp_min = einfo["locations"][user_location]["enemies"][user_enemy]["min_xp"]
      enemy_xp_max = einfo["locations"][user_location]["enemies"][user_enemy]["max_xp"]
      dg = einfo["locations"][user_location]["enemies"][user_enemy]["dg2"]
      enemy_xp = random.randint(enemy_xp_min, enemy_xp_max)
     #Skill Usage
      if enemy_dmg < 0:
        enemy_dmg = 0
      embd = discord.Embed(description="Choose one of the options and write it in the chat **WITHOUT THE PREFIX!**!\n\n\n\n\n**Fight**                           **Act**                           **Mercy**                   ")
      await asyncio.sleep(2)
      await ctx.send(embed=embd)
      def pred(m):
        return m.author == message.author and m.channel == message.channel
      try:
        answer1 = await bot.wait_for("message", check=pred, timeout=200)
        
        if answer1.content == "Fight" or answer1.content == "fight":
            #Lootbag# 10% chance to obtain one from an enemy.
              
            lootbag = random.randint(1, 10)
            damage = info["damage"]
            enemy_hp = user_enemy_hp
            
            
            
            #player attack
            enemy_hp_after = int(enemy_hp) - int(user_dmg) - int(damage)
            atem = discord.Embed(title="You Attack", description=f"You Damaged **{enemy_define}**, **-{user_dmg}HP** | current monster hp: **{enemy_hp_after}**", color=0xe74c3c)
            atem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803885802588733460/image0.png")
            await asyncio.sleep(3)
            await ctx.reply(embed=atem)
            if enemy_hp_after < 0:
                enemy_hp_after = 0
                await asyncio.sleep(3)
                femb=discord.Embed(description=f"You Won, Earned {enemy_gold}G and {enemy_xp}XP", color=0xe74c3c)
                await ctx.reply(embed=femb)
                info["selected_enemy"] = "None"
                info["enemyhp"] = 50
                info["in_fight"] = 0
                info["gold"] = info["gold"] + enemy_gold
                info ["exp"] = info["exp"] + enemy_xp
                if lootbag == 6:
                    await asyncio.sleep(3)
                    await ctx.reply(f"{ctx.author.mention} You got a lootbag, u?lootbag and see your!!")
                    info["lootbag"] = info["lootbag"] + 1
                    fileIO("players/{}/info.json".format(author.id), "save", info)
                info["enemieskilled"] = info["enemieskilled"] + 1
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await asyncio.sleep(3)
                await _check_levelup(ctx)
                break
                
            else:
                info["enemyhp"] = enemy_hp_after
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await asyncio.sleep(5)
                            
            #monster attack
            user_hp_after = int(user_hp) - int(enemy_dmg)
            gold_lost = random.randint(60, 220)
            atem = discord.Embed(title="Attack!", description=f"**{enemy_define}** Attacks, **-{enemy_dmg}HP** | current hp: **{user_hp_after}**", color=0xe74c3c)
            atem.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/803885802588733460/image0.png")
            await asyncio.sleep(3)
            await ctx.reply(embed=atem)
            
            
            
            
            if user_hp_after < 0:
                user_hp_after = 0
                info["gold"] = info["gold"] - gold_lost
                if info["gold"] < 0:
                    info["gold"] = 0
                info["deaths"] = info["deaths"] + 1
                info["health"] = 0
                info["in_fight"] = 0
                info["selected_enemy"] = "None"
                info["enemyhp"] = 50
                fileIO("players/{}/info.json".format(author.id), "save", info)
                
                await asyncio.sleep(3)
                femb=discord.Embed(description=f"**You Lost**\n\n**Stay Determines please!, You lost {gold_lost}G**")
                femb.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/804303928929812481/BA305022-ADCB-4DEE-84D5-01C54A1C85CF.gif")
                await asyncio.sleep(3)
                await ctx.reply(embed=femb)
                break
            else:
                info["health"] = user_hp_after
                fileIO("players/{}/info.json".format(author.id), "save", info)
                await asyncio.sleep(5)
                
        elif answer1.content == "Mercy" or answer1.content == "mercy":
            await asyncio.sleep(3)
            await spare_boss(ctx)
            break
          
        elif answer1.content == "Act" or answer1.content == "act":
            await asyncio.sleep(3)
            embed=discord.Embed(title="Acts", description="Choose:\n\n**Check\n\nHeal**")
            await ctx.send(embed=embed)
            def pred(m):
                return m.author == message.author and m.channel == message.channel
            try:
                answer1 = await bot.wait_for("message", check=pred, timeout=30)
        
                if answer1.content == "Check" or answer1.content == "check":
                    await asyncio.sleep(3)
                    embch=discord.Embed(title="Monster Stats", description=f"**{enemy_max_dmg}DMG, {dg}**")
                    await ctx.send(embed=embch)
                    await asyncio.sleep(6)
                if answer1.content == "Heal" or answer1.content == "heal":
                    await asyncio.sleep(3)
                    await heal_boss(ctx)
                    break
                else:
                    await asyncio.sleep(3)
                    await ctx.send("Choose a correct option next time!")
                    await asyncio.sleep(5)
            except asyncio.TimeoutError:
                    await asyncio.sleep(3)
                    info["in_fight"] = 0
                    fileIO("players/{}/info.json".format(author.id), "save", info)
                    await ctx.reply("You Missed!")
                    break
            
        else:
          await ctx.reply(f"Please choose one of the skills next time!")
          await asyncio.sleep(7)
            
            
      except asyncio.TimeoutError:
             info["in_fight"] = 0
             fileIO("players/{}/info.json".format(author.id), "save", info)
             await ctx.reply("You Missed!")
             break

#error handler
#account creator
async def _create_user(author):
    if not os.path.exists("players/{}".format(author.id)):
        os.makedirs("players/{}".format(author.id))
        new_account = {
            "name": author.name,
            "race": "None",
            "class": "None",
            "health": 100,
            "damage": 0,
            "max_health": 100,
            "enemyhp": 50,
            "in_fight": 0,
            "lvl": 1,
            "resets" : 0,
            "enemieskilled": 0,
            "deaths": 0,
            "selected_enemy": "None",
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
            "daily_block": 0,
            "rest_block": 0,
            "hp_potions": 4,
            "max_pot" : 12,
        }
        fileIO("players/{}/info.json".format(author.id), "save", new_account)
    info = fileIO("players/{}/info.json".format(author.id), "load")
    
#cogs loader
for filename in os.listdir('./cogs'):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print("Cogs Loaded!")

bot.run(config_location["Token"])
