from discord.ext import commands
import discord


class ChatManage(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount=100000):
		await ctx.channel.purge(limit=amount + 1)

	@commands.command()
	async def ping(self, ctx):
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Pong', icon_url=self.bot.user.avatar_url)
		embed.add_field(name=f'{round(self.bot.latency * 1000)}ms',
		                value='.')
		await ctx.send(embed=embed)

	@commands.command()
	async def cmessage(self, ctx, channel: discord.TextChannel = None):
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(
			name='Messages',
			icon_url=self.bot.user.avatar_url
		)
		channel = channel or ctx.channel
		count = 0
		async for _ in channel.history(limit=None):
			count += 1
		embed.add_field(
			name=channel.name,
			value=str(count),
			inline=True
	        )
		await ctx.send(embed=embed)

	@commands.command()
	async def members(self, ctx):
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(
			name='Members',
			icon_url=self.bot.user.avatar_url
		)
		member = list(self.bot.get_all_members())
		embed.add_field(
			name='.',
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


def setup(bot):
	bot.add_cog(ChatManage(bot))
