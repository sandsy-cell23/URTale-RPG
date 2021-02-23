import discord
from discord.ext import commands
from botTools.dataIO import fileIO
import time
from datetime import datetime
import DiscordUtils

starttime = time.time()

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def info(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        info = fileIO("config/config.json", "load")
        em = discord.Embed(title="My info:", type="rich", description=f"**An Advanced UNDERTALE RPG game\n\nGuilds Count:{len(self.bot.guilds)}\n\nbot Latency: {round(self.bot.latency * 1000)}ms\n\nBot Uptime:**\n`{days}d, {hours}h, {minutes}m, {seconds}s`", color = 0x979c9f)
        em.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.reply(embed=em)
        
    @commands.command()
    async def help(self, ctx):
        embed1 = discord.Embed(color=0x979c9f).add_field(name="**Commands**", value="Page 1")
        embed1.add_field(name="**u?help**", value="Shows the help list for commands intructions", inline=True)
        embed1.add_field(name="**u?start**", value="For those who didn't start the game yet, starting there journey", inline=True)
        embed1.add_field(name="**u?fight**", value="start a fight with a random mosnter depends on your location", inline=True)
        embed1.add_field(name="**u?heal**", value="Heals you outside the battle [potions needed]", inline=True)        
        embed1.add_field(name="**u?travel**", value="Travel Across towns and fight more greater monsters", inline=True)
        embed1.add_field(name="**u?fboss**", value="fight a boss monster random or 1 boss depends on your location", inline=True)
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/802902768842178560/5F799AF4-50A5-47A3-ADCB-2521F89CFEE7.png")
        embed2 = discord.Embed(color=0x979c9f).add_field(name="**Commands**", value="Page 2")
        embed2.add_field(name="**u?stats**", value="veiw your player stats and more", inline=True)
        embed2.add_field(name="**u?info**", value="Shows the bot info and more", inline=True)
        embed2.add_field(name="**u?shop**", value="Opens the shop to weapons and potions [depends on your location]", inline=True)
        embed2.add_field(name="**u?arshop**", value="Opens the armor shop to buy armor [depends on your location]", inline=True)
        embed2.add_field(name="**u?equip**", value="equip the weapons you bought from the shop", inline=True)
        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/802902768842178560/5F799AF4-50A5-47A3-ADCB-2521F89CFEE7.png")
        embed3 = discord.Embed(color=0x979c9f).add_field(name="**Commands**", value="Page 3")
        embed3.add_field(name="**u?armor**", value="equip the armor you bought from the armor shop", inline=True)
        embed3.add_field(name="**u?daily**", value="Get your daily prize with this command", inline=True)
        embed3.add_field(name="**u?vote**", value="Voting, There is an vote reward for top.gg platform (500G+)", inline=True)
        embed3.add_field(name="**u?gold**", value="To Check how much gold you have", inline=True)
        embed3.add_field(name="**u?text**", value="Enter some letters to get an undertale blank text box!", inline=True)
        embed3.add_field(name="**u?lb**", value="Check who is on top on gold currency!", inline=True)
        embed3.add_field(name="**u?don**", value="Donate and support URTale To last Longer *(even forever)*", inline=True)
        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/793382520665669662/802902768842178560/5F799AF4-50A5-47A3-ADCB-2521F89CFEE7.png")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔒', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3]
        await paginator.run(embeds)

        
    @commands.command()
    async def vote(self, ctx):
        vt = discord.Embed(
        title="<:D1:795979686635110451> Voting", color=0x2ecc71
        )
        vt.add_field(name="Vote on Top.gg (exclusive reward!)", value="[Click Here](https://top.gg/bot/781392003694067753)", inline=True)
        vt.add_field(name="vote on botsfordiscord", value="[Click Here](https://botsfordiscord.com/bot/781392003694067753)", inline=True)
        
        vt.add_field(name="Vote On Top.gg for our server (exclusive rewards)", value="[Click Here](https://top.gg/servers/790895387451588629)", inline=True)
        await ctx.send(embed=vt)
        
        
        
    @commands.command()
    async def invite(self, ctx):
        e = discord.Embed(description="[My Bot Invite!](https://discord.com/api/oauth2/authorize?client_id=781392003694067753&permissions=388160&scope=bot)\n\n[My Support Server!](https://discord.gg/ZrktueCZWF)")
        await ctx.send(embed=e)
        
    @commands.command()
    async def don(self, ctx):
        e = discord.Embed(description="**DONATE ON PATREON**\n[Click Me](http://patreon.com/URTale)")
        await ctx.send(embed=e)
    
    
    
    

def setup(bot):
    bot.add_cog(Info(bot))