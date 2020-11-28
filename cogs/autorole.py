import discord
from discord.ext import tasks,commands

class AutoRole(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    def get_role(self,id):
        return self.bot.get_guild(770964766592204801).get_role(id)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.message_id == 773057099725799424:
            await self.helper_or_learner(payload,"add")
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        if payload.message_id == 773057099725799424:
            await self.helper_or_learner(payload,"remove")
    
    
    async def helper_or_learner(self,payload, event):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)
        if emoji == "📖":
            role = guild.get_role(770967951859122188)
            try:
                if event == "add":
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)
            except:
                pass
            return
        if emoji == "✍️":
            role = guild.get_role(770966738954616872)
            try:
                if event == "add":
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)
            except:
                pass
            return

def setup(bot):
    bot.add_cog(AutoRole(bot))
    print("[Autorole] Loaded")