from discord.ext import commands
import discord


class ChatManage(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.extensions = extensions = [
			'cogs.errorcatch',
			'cogs.webscraping',
			'cogs.funcogs',
			'cogs.modcog',
			'cogs.events',
			'cogs.helpcog',
			'cogs.chatmanage',
			'cogs.math'
		]

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount=100000):
		await ctx.channel.purge(limit=amount + 1)

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f'{round(self.bot.latency * 1000)}ms')

	@commands.command()
	async def cmessage(self, ctx, channel: discord.TextChannel = None):
		embed = discord.Embed(
			color=discord.Color.green()
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
		embed.set_image(url='https://i.imgur.com/J1auBSs.png')

		await ctx.send(embed=embed)

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


def setup(bot):
	bot.add_cog(ChatManage(bot))
