import discord
from discord.ext import commands
from datetime import datetime
from discord.ext.commands import MissingPermissions, CommandNotFound, BotMissingPermissions, MissingRequiredArgument

class ErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, message, error):
		if isinstance(error, commands.CommandOnCooldown):
			left = round(error.retry_after, 2)
			if error.cooldown.type == commands.BucketType.user:
				await message.send(f"This command is ratelimited, please try again in {left} .")
			elif error.cooldown.type == commands.BucketType.guild:
				await message.send(f"{left} seconds left until this server can use this command again.")
			elif error.cooldown.type == commands.BucketType.member:
				await message.send(f"You have {left} seconds left until you can use this command in this server again.")
			elif error.cooldown.type == commands.BucketType.channel:
				await message.send(f"{left} seconds left until this channel can use this command again.")
			else:
				await message.send(f"There is no cooldown message set for this cooldown type.")

		elif isinstance(error, commands.NoPrivateMessage):
			await message.send("You cannot use this command in direct messages!")
		elif isinstance(error, commands.MissingPermissions):
			await message.send("You are missing some required permissions.")
		elif isinstance(error, commands.BotMissingPermissions) or "Missing Permissions" in str(error):
			await message.send("I don't have permission to do this!")
		elif isinstance(error, commands.CommandNotFound):
			await message.send("That command doesn't exist!")
		elif isinstance(error, commands.MemberNotFound):
			await message.send("Member not found !")
		elif isinstance(error, commands.UserNotFound):
			await message.send("User not found !")
		elif isinstance(error, commands.MissingRequiredArgument):
			await message.send("Something is missing !")
		
		elif isinstance(error, commands.RoleNotFound):
			await message.send("Role not found !")
   
		else:
			channel = discord.utils.get(self.bot.get_all_channels(), id=945347264212250644)
			await channel.send(f"The bot owner can see more in the bot logs.\n```{error}```")
			f = open('log.txt', 'a')
			f.write(str(datetime.now()) + ' : Error occured :\n %s\n\n' % error)
			f.close()
			raise error

def setup(bot):
	bot.add_cog(ErrorHandler(bot))