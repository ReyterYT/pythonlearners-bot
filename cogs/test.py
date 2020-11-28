import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def err(self,ctx):
        await ctx.send([][0])

def setup(bot):
    bot.add_cog(Test(bot))
    print("[Test] Loaded")