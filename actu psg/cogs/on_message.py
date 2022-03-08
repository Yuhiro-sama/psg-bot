import discord
from discord.ext import commands
from utils.db_userinf import *

class On_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if not message.guild:
            return
        if message.author.name == self.bot.user.name:
            return
        
        if get_all_by_serv(message) == []:
            insert_user(message)
            
            
        update_user(message, "xp", 5)
        update_user(message,"coin", 3)
        update_user(message, "msg", 1)
        check_lvl(message)
        
        
def setup(bot):
    bot.add_cog(On_msg(bot))