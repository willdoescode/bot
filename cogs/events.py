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
		channel = discord.utils.get(self.bot.get_all_channels(), name='logs')
		embed.add_field(
			name=f'{self.bot.user.name}',
			value='Has connected'
		)
		await channel.send(embed=embed)
		print('Servers connected to:')

		for server in self.bot.servers:
			print(server.name)

		print(f'{self.bot.user.name} has connected to discord')

	@commands.Cog.listener()
	async def on_member_join(self, ctx, member: discord.Member):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		channel = discord.utils.get(self.bot.get_all_channels(), name='joins-and-leaves')
		embed.add_field(
			name='Welcome to the server:',
			value=f'@{member}',
			inline=False
		)
		await channel.send(embed=embed)
		role = discord.utils.get(ctx.guild.roles, name='new player')
		await member.add_roles(role)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = discord.utils.get(self.bot.get_all_channels(), name='joins-and-leaves')
		await channel.send(f'Sad to see you go @{member}')


def setup(bot):
	bot.add_cog(Events(bot))
