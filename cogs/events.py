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
					async for guilds in self.bot.fetch_guilds(limit=150):
						print(f'{self.bot.user.name} has connected to {guilds.name} server')

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		server = member.guild
		try:
			for channel in server.text_channels:
				if channel.name == 'joins-and-leaves':
					embed.add_field(
						name='Welcome To The Server',
						value=member.display_name
					)
					await channel.send(embed=embed)
					embed = discord.Embed(
						color=discord.Color.green()
					)
		except:
			print('no joins and leaves channel')


def setup(bot):
	bot.add_cog(Events(bot))
