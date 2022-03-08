import discord
from discord.ext import commands
import asyncio
import json
import math
import discord
from utils.db_userinf import *
from discord.ext import commands



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def getConfig_role(guildID):
    with open("xp.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["role"]:
        return None
    return data["role"][str(guildID)]

def try_config_role(guildID, coins):
    with open("xp.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["role"]:
        defaultConfig = {
            "price" : coins
        }
        updateConfig_role(guildID, defaultConfig)
        return True
    return False

def updateConfig_role(guildID, data):
    with open("xp.json", "r") as config:
        config = json.load(config)
    config["role"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("xp.json", "w") as config:
        config.write(newdata)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class Purchase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_role_shop(self, ctx, role : discord.Role, coins :int):
        if role.permissions.administrator is True:
            return await ctx.send("You can't add role with admin permissions to the shop ! ")
        try:
            r = try_config_role(role.id, coins)
            if r == True:
                return await ctx.send(f"Succesfullt added **{role.name}** role to the shop .")
            if r == False:
                return await ctx.send("This role is already in the shop .")
        except:
            print("error !")
            
    @commands.command()
    async def buy_shop_role(self, ctx,*, role: discord.Role=None):
        if role is None:
            return
        if role in ctx.author.roles:
            return await ctx.send("You already have this roles !")
        
        roles = getConfig_role(role.id)
        if roles is None:
            return await ctx.send(f"This role are not on the shop !")
        
        price = int(roles["price"])
        
        coin  = get_user_serv(ctx.author, "coin")
        if price > coin:
            return await ctx.send(f"You don't have enough coins to buy this role ! You need {price - coin} more coins")
        
        await ctx.author.add_roles(role)
        await update_user(ctx.author, -price)
        await ctx.send("Successful transaction ! ")
        
    @commands.command()
    async def shop_role(self, ctx):
        colour = ctx.guild.me.top_role.colour
        with open("xp.json", "r") as config:
            data = json.load(config)
        a = discord.Embed(title=f"Shop of {ctx.guild.name}", colour=colour)
        if data["role"] is None:
            return await ctx.send("No role in the shop !")
        
        for role in data["role"]:
            roles = discord.utils.get(ctx.guild.roles, id=int(role))
            if roles is None:
                continue
            price = data["role"][str(role)]["price"]
            a.add_field(name = f'{roles.name}', value = f'Price : {price}', inline=False)
            
        await ctx.send(embed=a)

def setup(bot):
    bot.add_cog(Purchase(bot))