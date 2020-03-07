from discord.ext import (
	commands,
	tasks,
)
from itertools import cycle
import discord
from datetime import datetime


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.status = cycle(['with your toys', 'with a dog', ' a guitar', 'csgo',
		                    'with fire', 'with your feeling', 'on my own', 'a song',
		                     'with bot things', 'oil changing simulator'])

	@tasks.loop(seconds=1)
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
		embed.set_author(
			name='Connected!',
			icon_url=self.bot.user.avatar_url
		)
		embed.set_author(name='Log', icon_url=self.bot.user.avatar_url)
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				if channel.name == 'logs':
					embed.add_field(
						name=f'{self.bot.user.name}',
						value=f'Has connected'
					)
					await channel.send(embed=embed)
					embed = discord.Embed(
						color=discord.Color.green()
					)
		async for guilds in self.bot.fetch_guilds(limit=150):
			print(f'{self.bot.user.name} bot has connected to {guilds.name} server')

	@commands.Cog.listener()
	async def on_member_join(self, member):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		embed.set_author(name='Welcome to the server', icon_url=self.bot.user.avatar_url)
		server = member.guild
		try:
			for channel in server.text_channels:
				if channel.name == 'joins-and-leaves':
					embed.add_field(
						name='--------',
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
