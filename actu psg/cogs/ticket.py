import discord
from discord.ext import commands
from discord.errors import Forbidden
import aiofiles

color = 0xff1100


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.reaction_roles = []
    
    @commands.command()
    async def ticket(self, ctx):
        ticket_embed = discord.Embed(title="Ticket", description="Réagissez pour ouvrir un ticket", color=color)
        msg = await ctx.send(embed=ticket_embed)
        await msg.add_reaction("🎫")
        emoji = "🎫"
        self.bot.reaction_roles.append((ctx.guild.id, msg.id, str(emoji.encode("utf-8"))))
            
        async with aiofiles.open("reaction_roles.txt", mode="a") as file:
            emoji_utf = emoji.encode("utf-8")
            await file.write(f"{ctx.guild.id} {msg.id} {emoji_utf}\n")

        
        
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for guild_id, msg_id, emoji in self.bot.reaction_roles:
            guild = self.bot.get_guild(guild_id)
            if payload.member.name == self.bot.user.name:
                return
            for channel in guild.text_channels:
                memb = str(payload.member.name).lower()
                if channel.name == f"ticket-{memb}":
                    return
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                try:
                    p = await guild.create_text_channel(f"ticket-{payload.member.name}")
                    await p.send(f"{payload.member.mention} opened a ticket")
                except Forbidden:
                    await payload.member.send("I don't have the rights to do this, please contact an administrator.")
                    return
            
            
        
        
        

def setup(bot):
    bot.add_cog(Ticket(bot))