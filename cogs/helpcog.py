from discord.ext import commands
import discord
import json


class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		with open('help.json') as f:
			self.help_commands = json.load(f)
		with open('help1.json') as f:
			self.help1_commands = json.load(f)

	@commands.command()
	async def help(self, ctx):

		alsoembed = discord.Embed(
			color=discord.Color.orange(),
			timestamp=ctx.message.created_at
		)

		embed = discord.Embed(
			color=discord.Color.orange()
		)

		embed.set_author(
			name='Help is here',
			icon_url=self.bot.user.avatar_url
		)

		for name, value in self.help_commands.items():
			embed.add_field(name=name, value=value, inline=False)

		for names, values in self.help1_commands.items():
			alsoembed.add_field(name=names, value=values, inline=False)
		person = ctx.author
		await person.send(embed=embed)
		await person.send(embed=alsoembed)
		await ctx.send('Sent help to your dms! :thumbsup:')


def setup(bot):
	bot.add_cog(Help(bot))
