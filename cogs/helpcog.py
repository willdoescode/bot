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
	async def help(self, ctx, command=None):

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

		for value in self.help_commands['help']:
			embed.add_field(
				name=str(value),
				value=self.help_commands[value]['use'],
				inline=True
			)

		for value in self.help1_commands['help']:
			alsoembed.add_field(
				name=str(value),
				value=self.help1_commands[value]['use'],
				inline=True
			)
		person = ctx.author
		await person.send(embed=embed)
		await person.send(embed=alsoembed)
		await ctx.send('Sent help to your dms! :thumbsup:')


def setup(bot):
	bot.add_cog(Help(bot))
