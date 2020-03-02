from discord.ext import commands
import discord
import logging

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class ErrorCatch(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			logger.error(error)
			await ctx.send('Invalid command')

		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			logger.error(error)
			await ctx.send('Invalid Permissions')

		elif isinstance(error, discord.ext.commands.errors.BadArgument):
			logger.error(error)
			await ctx.send('Please use the commands properly, dm @PieTales#0495 if you need help')

		elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
			logger.error(error)
			await ctx.send('Please finish the command')

		elif isinstance(error, RuntimeError):
			logger.error(error)
			await ctx.send('please enter your command correctly')

		elif isinstance(error, RuntimeWarning):
			logger.error(error)
			await ctx.send('Coder is Stupid and Forgot to Await Something in the code')


def setup(bot):
	bot.add_cog(ErrorCatch(bot))
