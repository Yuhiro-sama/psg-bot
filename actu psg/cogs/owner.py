from turtle import color
import discord
from discord.ext import commands
import requests

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    
    def is_owner():
        async def predicate(ctx):
            owner_ids = [636891228876570634, 702136277910159401]
            if str(ctx.author.id) in owner_ids:
                return True
            else:
                return False
        return commands.check(predicate)
        
    @commands.command(name="username")
    @is_owner()
    async def change_username(self, ctx, *, name: str):
        """ Change username. """
        try:
            await self.bot.user.edit(username=name)
            await ctx.send(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(err)
    
    @commands.command(name="avatar")
    @is_owner()
    async def change_avatar(self, ctx, url):
        """ Change avatar. """
        try:
            data = requests.get(url).content
            await self.bot.user.edit(avatar=data)
            await ctx.send(f"Successfully changed avatar")
        except:
            await ctx.send("only jpg and png accepted")

def setup(bot):
    bot.add_cog(owner(bot))