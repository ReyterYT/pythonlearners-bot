import discord
import asyncio
from discord.ext import commands
import typing

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    async def mute(self, bot, who, role, delay):
        await who.add_roles(role)
        await asyncio.sleep(delay)
        try:
            await who.remove_roles(role)
        except Exception as e:
            print(e)
    
    async def lock(self, bot, channel, role, delay):
        perms = {role: discord.PermissionOverwrite(send_messages=False)}
        await channel.edit(overwrites=perms)
        await asyncio.sleep(delay)
        perms = {role: discord.PermissionOverwrite(send_messages=True)}
        await channel.edit(overwrites=perms)
        return channel
    
    def _lock_callback(self,fut):
        self.bot.loop.create_task(fut.result().send("Unlocked channel!"))
        
    @commands.command(name="lock")
    @commands.is_owner()
    async def _lock(self,ctx):
        task = self.bot.loop.create_task(self.lock(self.bot, ctx.channel, ctx.guild.default_role, 300))
        task.add_done_callback(self._lock_callback)
        await ctx.send("Locked channel!")
    
    @commands.command(name="mute",usage="<member> [reason]")
    @commands.is_owner()
    async def _mute(self,ctx,member:discord.Member,duration:typing.Union[int,str]=None,reason=None):
        if reason is None and isinstance(duration,str):
            reason = duration
            duration = 10
        if duration is None:
            duration = 10
        role = ctx.guild.get_role(771720829679566848)
        if role in member.roles:
            await ctx.send("Member is already muted")
            return
        if member.guild_permissions.administrator:
            await ctx.send("That member is one of the adminstrator and my tape won't work on them")
            return
        if member.top_role > ctx.me.top_role:
            await ctx.send("That member role is higher than mine")
            return
        self.bot.loop.create_task(self.mute(self.bot,member,role, duration))
        await ctx.send(f"Muted **{member}** for {duration}s")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self,ctx,member:discord.Member,reason=None):
        """
        Kick a member from the server
        """
        if member == ctx.author:
            await ctx.send("You can't kick yourself silly")
            return
        if member == ctx.me:
            await ctx.send("I can leave myself if you want rather than kicking me")
            return
        if member.guild_permissions.administrator:
            await ctx.send("That member is Adminstrator and i can't kick them")
            return
        if member.top_role > ctx.me.top_role:
            await ctx.send(f"**{member}** role is higher than me, and i can't interact with them")
            return
        try:
            await member.kick(reason=reason)
            await ctx.send(f"Successfully kicked **{member}** 👌")
        except:
            await ctx.send("Something went wrong while kicking member, try again")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,ctx,member:discord.Member,reason=None):
        """
        Ban a member from the server
        """
        if member == ctx.author:
            await ctx.send("You can't ban yourself silly")
            return
        if member == ctx.me:
            await ctx.send("You can't ban me")
            return
        if member.guild_permissions.administrator:
            await ctx.send("That member is Adminstrator and i can't ban them")
            return
        if member.top_role > ctx.me.top_role:
            await ctx.send(f"**{member}** role is higher than me, and i can't interact with them")
            return
        try:
            await member.kick(reason=reason)
            await ctx.send(f"Successfully banned **{member}** 👌")
        except:
            await ctx.send("Something went wrong while banning member, try again")
            
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount:int):
        """
        Purge/Clear a textchannel messages depending on the argument provided to **amount** if amount is bigger than 1000 it will automatically set to 1000
        """
        msg = ""
        if amount > 1000:
            msg = "Note: cannot purge more than 1000 messages\n"
            amount = 1000
        async with ctx.typing():
            deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(msg+f"Deleted {len(deleted)} messages!",delete_after=5)

def setup(bot):
    bot.add_cog(Moderation(bot))
    print("[Admin] Loaded")