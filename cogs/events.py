from discord.ext import (
	commands,
	tasks,
)
from itertools import cycle
import discord


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.status = status = cycle(['with your toys', 'with a dog', ' a guitar', 'csgo',
		                              'with fire', 'with your feeling', 'on my own', 'a song',
		                              'with bot things', 'oil changing simulator'])

	@tasks.loop(seconds=2)
	async def big(self):
		await self.bot.change_presence(
			status=discord.Status.idle,
			activity=discord.Game(next(self.status))
		)

	@commands.Cog.listener()
	async def on_ready(self):
		self.big.start()
		embed = discord.Embed(
			color=discord.Color.green()
		)
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				if channel.name == 'logs':
					embed.add_field(
						name=f'{self.bot.user.name}',
						value='Has connected'
					)
					await channel.send(embed=embed)
					embed = discord.Embed(
						color=discord.Color.green()
					)
					print(f'{self.bot.user.name} has connected to discord')
		async for guild in self.bot.fetch_guilds(limit=150):
			print(guild.name)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = discord.utils.get(self.bot.get_all_channels(), name='joins-and-leaves')
		await channel.send(f'Sad to see you go @{member}')


def setup(bot):
	bot.add_cog(Events(bot))
