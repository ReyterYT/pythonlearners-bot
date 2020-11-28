import discord
import time
import datetime
import psutil
import asyncio
from discord.ext import commands

class Help(commands.MinimalHelpCommand):
    def get_command_signature(self,cmd):
        alias = '|'.join(cmd.aliases)
        if alias:
            alias = "|"+alias
        return f"```[{cmd.qualified_name}{alias}]```"

class Utility(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        """bot.help_command = Help()
        bot.help_command.cog = self
        bot.help_command.aliases_heading = None"""
    
    @commands.command()
    async def info(self,ctx):
        count = psutil.cpu_count()
        freq = psutil.cpu_freq()
        embed = discord.Embed(title="Bot information", description=f"Created by **{self.bot.get_user(self.bot.owner_id)}**\nCreated at **{str(self.bot.user.created_at).split('.')[0]}**")
        embed.add_field(name="CPU",value=f"Count: **{count}**\nCurrent Frequency: **{freq.current}**\nMax Frequency: **{freq.max}**\nMin Frequency: **{freq.min}**")
        embed.add_field(name="Bot statistics",value=f"Users: **{len(self.bot.users)}**\nMessage cache: **{len(self.bot.cached_messages)}**")
        await ctx.send(embed=embed)
    
    @commands.command(usage="<list of members>")
    async def members(self,ctx,members:commands.Greedy[int]):
        members = [ctx.guild.get_member(i) for i in members]
        members = [i for i in members if not i is None]
        embed = discord.Embed(title="Member list", description="\n".join([f"{i.mention}({str(i)})" for i in members]) or "NaN")
        await ctx.send(embed=embed)
    
    @commands.command(name="offtopics",aliases=["ot"])
    async def off_topic(self, ctx):
        await ctx.send("Please use <#771013066926063647> for off topics, thank you.")
    
    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def ping(self,ctx):
        """
        Shows the bot latency
        """
        tic_typing = time.perf_counter()
        async with ctx.typing():
            toc_typing = time.perf_counter()
        embed = discord.Embed(description="loading.....")
        tic_msg = time.perf_counter()
        msg = await ctx.send(embed=embed)
        toc_msg = time.perf_counter()
        embed.add_field(name="Typing latency",value=f"{int((toc_typing-tic_typing)*1000)}ms", inline=False)
        embed.add_field(name="Bot latency",value=f"{int((toc_msg-tic_msg)*1000)}ms",inline=False)
        embed.add_field(name="Webhook latency",value=f"{int(self.bot.latency*1000)}ms")
        embed.description = None
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
    print("[Utility] Loaded")