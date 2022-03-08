import discord
from discord.ext import commands
from utils.db_userinf import *
import sqlite3


conn = sqlite3.connect('storage.db')
c = conn.cursor()

class db_user_inf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.member = []
        self.ad = 0
    
    
    @commands.command()
    async def rank(self, ctx,*,  user : discord.Member= None):
        
        if check_bot(user) is False:
            return await ctx.send("Bot aren't ranked !")
        
        user = user or ctx.author
        
        try :
            a = get_all_by_serv(user)
            a[0]
            pass
        except:
            return await ctx.send("This user are not ranked")
        lvl = get_user_serv(user, "lvl")
        msg = get_user_serv(user, "msg")
        coin  = get_user_serv(user, "coin")
        
        if user == ctx.author:
            embed = discord.Embed(title = f"{user.name}", description=f"> You are level: `{lvl}`\n> You sent: `{msg}` message(s)\n> You have: `{round(coin)}` coin(s)", color=color)
        else:
            embed = discord.Embed(title = f"{user.name}", description=f"> `{user.name}` are level: `{lvl}`\n> {user.name} sent: `{msg}` message(s)\n> {user.name} has: `{round(coin)}` coin(s)", color=color)
            
        await ctx.send(embed=embed)
        
    
    @commands.group(pass_context=True, invoke_without_command=True)
    async def top(self, ctx):
        top = []
        try:
            all = get_all_server(ctx)
        except:
            return all == None
        for element in all:
            user = await self.bot.fetch_user(element[1])
            self.member.append({'server':ctx.guild.id, 'user': user.id, 'lvl':get_user_serv_cus(user.id, ctx.guild.id, "lvl")})
            
            
        def get_lvl(uss):
            for r in uss:
                r.get('lvl')
        
        
        top.append(self.member)
        top.sort(key=get_lvl, reverse=True)
        
        
        n_list = -1
        c = add_top(ctx, top,n_list)
        
        
        if await check_rank(ctx, top, 'lvl') is False:
            self.member = []
            return 
        
        top_embed = discord.Embed(title="",color=color, timestamp=ctx.message.created_at)
        top_embed.set_author(name=ctx.guild.name + " - Classement 🏆 !", icon_url=f"{ctx.author.avatar_url}")
        top_embed.add_field(name="\u200b",value=f"\n".join([f"**{count}.**<@{row['user']}> - niveau : **{row['lvl']}**" for count, row in enumerate(top[c], start=1)]), inline=False )
        
        
        await ctx.send(embed=top_embed)
        self.member = []
        
        
        
def setup(bot):
    bot.add_cog(db_user_inf(bot))