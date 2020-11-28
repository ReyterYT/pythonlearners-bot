import discord
import traceback
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,err):
        if isinstance(err,commands.CommandNotFound):
            return
        err = getattr(err,"original",err)
        message = "```py\n"+"".join(traceback.format_exception(type(err),err,err.__traceback__))+"```"
        channel = self.bot.get_channel(782040010068459530)
        if channel is None:
            return
        await ctx.send("An error have occurred! don't worry we'll fix this soon")
        await channel.send(f"from command: `{ctx.command.name}`\n"+message)
        
def setup(bot):
    bot.add_cog(Events(bot))
    print("[Events] Loaded")