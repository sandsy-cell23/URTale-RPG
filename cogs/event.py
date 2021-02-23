import discord
from discord.ext import commands
import os
from discord.ext.commands import CommandNotFound

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
              
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mention in message.content.split():
            if message.author.bot:
                return
            await message.channel.send('Hey Fella!, my Prefix is **u?**')
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(799865869181255701)
        await channel.send(f"Joined a Server, {guild.name}\n\nMember Count: {guild.member_count}\n\nID: {guild.id}\n\n Owner: {guild.owner}")
    
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(799865869181255701)
        await channel.send(f"Left a Server, **{guild.name}**")
        
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            print("Someone is using an unknown command")
            return
        if isinstance(error, commands.CommandOnCooldown):
            print("Someone is using the command on cooldown")
            return
        raise error
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Players on {len(self.bot.guilds)} Servers"))

    
        

           

def setup(bot):
    bot.add_cog(Event(bot))