import discord
from discord.ext import tasks,commands

class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.get_channel.start()
    
    def cog_unload(self):
        self.get_channel.cancel()
    
    @tasks.loop(seconds=10)
    async def get_channel(self):
        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(773040761049710633)
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.guild.id == 770964766592204801:
            return
        if member.bot:
            return
        embed = discord.Embed(title=f"Welcome to {member.guild.name}", description=f"Welcome **{member}** This server is only for coders and learners we have python important but we will soon start to teach even other languages hope you all enjoy! 😃")
        embed.set_thumbnail(url=member.avatar_url)
        await self.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
    print("[Welcome] Loaded")