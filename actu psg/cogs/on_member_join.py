import discord
from discord.ext import commands
from utils.db_userinf import *

class On_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if get_all_by_serv(member) == []:
            insert_user(member)
        
        print(get_all_by_serv(member))
        
        
def setup(bot):
    bot.add_cog(On_msg(bot))