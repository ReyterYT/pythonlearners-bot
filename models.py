import discord
from discord.ext import commands
import aiomysql
import os
import asyncio
import json
import dotenv

dotenv.load_dotenv()

db_config = json.loads(os.getenv("MYSQL"))

class PythonLearners(commands.Bot):
    
    def __repr__(self):
        return f"<{type(self).__name__} users={len(self.users)} messages={len(self.cached_messages)}>"
    
    async def __setup_db(self):
        await self.wait_until_ready()
        self.db = await aiomysql.create_pool(**db_config)
        print("[Database] Established a pool connection")
    
    def __init__(self,*args,**kwargs):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.__setup_db())
        super().__init__(*args,intents=discord.Intents.all(),**kwargs)
    
    async def close(self,*args,**kwargs):
        self.db.close()
        await self.db.wait_closed()
        print("[Database] Closed pool connection")
        await super().close(*args,**kwargs)