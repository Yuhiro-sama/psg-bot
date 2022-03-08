import discord
from discord.ext import commands
from utils.db_userinf import *
import sqlite3
import aiofiles

conn = sqlite3.connect('storage.db')
c = conn.cursor()

class On_ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Hey I'm " + self.bot.user.name + ", you're my creator ? Oh i like you too much !!!")
        try:  
            c.execute("""CREATE TABLE user_inf (
                        guild_id text,
                        user_id text,
                        xp integer,
                        lvl integer,
                        msg integer,
                        coin float
                        )""")
        except:
            pass
        
        async with aiofiles.open("reaction_roles.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                self.bot.reaction_roles.append((int(data[0]), (int(data[1])), data[2].strip("\n")))
        
        
def setup(bot):
    bot.add_cog(On_ready(bot))