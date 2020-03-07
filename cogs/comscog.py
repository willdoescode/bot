import discord
from discord.ext import commands


class Commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def servers(self, ctx):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		embed.set_author(name='Connected Servers', icon_url=self.bot.user.avatar_url)
		async for guilds in self.bot.fetch_guilds(limit=150):
			embed.add_field(name=guilds.name, value='status: Connected', inline=False)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Commands(bot))

