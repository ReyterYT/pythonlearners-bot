import discord
from discord.ext import commands
import os
import dotenv
import models

dotenv.load_dotenv()

bot = models.PythonLearners(command_prefix="py!",case_insensitive=True,owner_ids=[716503311402008577],embed_color=discord.Color.from_rgb(52, 152, 219),help_command=None)
bot.load_extension("jishaku")
os.system("clear")

for ext in {"utility","admin","welcome","autorole","help","events","test"}:
    bot.load_extension("cogs."+ext)
    
@bot.listen()
async def on_ready():
    print("[Bot] Fetched needed cache")

@bot.listen()
async def on_message(msg):
    if msg.content in [f"<@{bot.user.id}>",f"<@!{bot.user.id}>"]:
        await msg.channel.send(f"Hello! my prefix is `{bot.command_prefix}`")

bot.run(os.getenv("TOKEN"))
