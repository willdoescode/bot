from discord.ext import commands
import discord


class ChatManage(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount=100000):
		await ctx.channel.purge(limit=amount)

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'{round(self.bot.latency * 1000)}ms')

	@commands.command()
	async def cmessage(self, ctx, channel: discord.TextChannel = None):
		channel = channel or ctx.channel
		count = 0
		async for _ in channel.history(limit=None):
			count += 1
		await ctx.send(f'There are {count} messages in {channel.mention}')

	@commands.command()
	async def members(self, ctx):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		member = list(self.bot.get_all_members())
		embed.add_field(
			name='Amount of members:',
			value=f'{len(member)}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def yell(self, ctx, *, message=None):
		await ctx.send(f'@everyone {message}')

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def yell_here(self, ctx, *, message=None):
		await ctx.send(f'@here {message}')

	@commands.command()
	async def connected_servers(self, ctx):
		servers = list(self.bot.servers)
		embed = discord.Embed(
			color=discord.Color.green()
		)
		for server in servers:
			embed.add_field(name=f'{server}', value='')
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(ChatManage(bot))
