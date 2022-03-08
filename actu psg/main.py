
import sqlite3
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"), intents=intents)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)