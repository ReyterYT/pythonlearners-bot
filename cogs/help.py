import discord
from discord.ext import commands
import inspect
import datetime

class CommandOrCategory(commands.Converter):
    async def convert(self,ctx,arg):
        bot = ctx.bot
        res = bot.cogs.get(arg) or bot.get_command(arg) or False
        res = [res]
        res.insert(0,arg)
        return res

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    def get_syntax(self,cmd):
        params = cmd.clean_params
        _params = []
        alias = cmd.aliases
        if len(alias) == 0:
            alias = cmd.qualified_name
        else:
            alias.insert(0,cmd.qualified_name)
            alias = "|".join(alias)
        for param in params.values():
            if param.default == inspect._empty:
                _params.append(f"<{param.name}>")
                continue
            _params.append(f"[{param.name}]")
        return f"{alias} {cmd.usage or ' '.join(_params)}"
        
    
    async def get_cmds(self,ctx,cog):
        cmds = cog.get_commands()
        _commands = []
        for cmd in cmds:
            try:
                await cmd.can_run(ctx)
            except:
                continue
            _commands.append(self.get_syntax(cmd))
        return _commands or None
            
   
    @commands.command(name="help",usage="[command|category]")
    async def help1(self,ctx,*,arg: CommandOrCategory=None):
        """
        Show this!
        """
        if not arg is None:
            name = arg[0]
            arg = arg[1]
        if arg is None:
            cmds = self.bot.commands
            _cmds = [i.name for i in self.bot.commands]
            _cmds.sort()
            for cmd in _cmds:
                for names in cmds:
                    if names.name == cmd:
                        _cmds[cmd.index(cmd)] = names
            cogs = dict()
            for cmd in cmds:
                try:
                    await cmd.can_run(ctx)
                except:
                    continue
                try:
                    cogs[cmd.cog_name or "Uncategorized"].append(cmd)
                except KeyError:
                    cogs[cmd.cog_name or "Uncategorized"] = [cmd]
            cogs = cogs.items()
            embed = discord.Embed(title="Help", description="Show help for every command the bot currently have")
            for name,_commands in cogs:
                embed.add_field(name=name,value=",".join([f"`{i.name}`" for i in _commands]),inline=False)
            await ctx.send(embed=embed)
            return
        if arg == False:
            await ctx.send(f'command or category {name} not found')
            return
        if not isinstance(arg,commands.Cog):
            try:
                await arg.can_run(ctx)
                syntax = "```css\n"+self.get_syntax(arg)+"```"
                embed = discord.Embed(title=f"Help for {arg.name}", description=syntax, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="description",value=arg.help or "No description provided")
                embed.add_field(name="category",value=arg.cog_name or "Uncategorized")
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f'command or category {name} not found')
        else:
            _commands_raw = arg.get_commands()
            _commands = []
            for cmd in _commands_raw:
                try:
                    await cmd.can_run(ctx)
                except:
                    continue
                _commands.append(cmd)
            if len(_commands) == 0:
                await ctx.send(f"command or category {name} not found")
                return
            embed = discord.Embed(title=f"Category {arg.__class__.__name__}", description="\n".join([i.name for i in _commands]))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print("[Help] Loaded")