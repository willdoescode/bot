from discord.ext import commands
import discord


class ErrorCatch(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send('Invalid command')
		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			await ctx.send('Invalid Permissions')
		elif isinstance(error, discord.ext.commands.errors.BadArgument):
			await ctx.send('Please use the commands properly, dm @PieTales#0495 if you need help')
		elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
			await ctx.send('Please finish the command')
		elif isinstance(error, RuntimeError):
			await ctx.send('please enter your command correctly')
		elif isinstance(error, RuntimeWarning):
			await ctx.send('Coder is Stupid and Forgot to Await Something in the code')


def setup(bot):
	bot.add_cog(ErrorCatch(bot))


