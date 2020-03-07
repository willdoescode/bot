from discord.ext import commands
import discord
import requests
import random
import json


class FunCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.responses = [
			'It is certain.',
			'It is decidedly so.',
			'Without a doubt.',
			'Yes - definitely.',
			'You may rely on it.',
			'As I see it, yes.',
			'Most likely.',
			'Outlook good.',
			'Yes.',
			'Signs point to yes.',
			'Don\'t count on it.',
			'My reply is no.',
			'Better not tell you now.',
			'Concentrate and ask again.',
			'Very doubtful.'
		]
		with open('jokes.json', 'r') as f:
			self.jokes = json.load(f)

	@commands.command()
	async def pun(self, ctx):
		joke = random.choice(self.jokes)
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Joke', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name='--------',
			value=f'{joke}',
			inline=False
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def expand(self, ctx, link):
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Link', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=f'{link}',
			value=f'Expanded: {requests.get(link).url}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def coinflip(self, ctx):
		embed = discord.Embed(
			color=discord.Color.purple(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Coin says:', icon_url=self.bot.user.avatar_url)
		ok = ['heads', 'tails']
		embed.add_field(
			name='--------',
			value=f'{random.choice(ok)}',
			inline=False
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def show_code(self, ctx):
		await ctx.author.send('https://i.imgur.com/qIKR0Qt.gif lol you thought')

	@commands.command(aliases=['pfp'])
	async def avatar(self, ctx, member: discord.Member):
		show_avatar = discord.Embed(
			color=discord.Color.dark_red(),
			timestamp=ctx.message.created_at
		)
		show_avatar.set_author(name='Avatar', icon_url=self.bot.user.avatar_url)
		show_avatar.set_image(
			url=member.avatar_url
		)
		show_avatar.add_field(
			name=member.display_name,
			value='--------',
			inline=True
		)
		await ctx.send(embed=show_avatar)

	@commands.command()
	async def dm(self, ctx):
		await ctx.author.send('I done slid into your dms')
		await ctx.send(f'sliding into {ctx.author}\'s dms')

	@commands.command(aliases=['8ball'])
	async def _8ball(self, ctx, *, question):
		embed = discord.Embed(
			color=discord.Color.purple(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name=' Magic 8ball', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=f'{ctx.author} has asked: {question}',
			value=f'Answer: {random.choice(self.responses)}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def getinfo(self, ctx, member: discord.Member):
		name = member.display_name
		status = member.status
		joined = member.joined_at
		activity = member.activity
		roles = member.roles
		guild = member.guild
		embed = discord.Embed(
			color=discord.Color.red(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='User Info', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=name,
			value=f'joined: {joined}\nstatus: {status}\nactivity: {activity}\nroles: '
			      f'{roles}\nguild: {guild}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command(aliases=['embed'])
	async def em(self, ctx, *, message: str):
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Embed Created', icon_url=self.bot.user.avatar_url)
		embed.add_field(name=ctx.author, value=message, inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def nick(self, ctx, member: discord.Member, *, nickname):
		embed = discord.Embed(
			color=discord.Color.purple(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Nickname', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=member.display_name,
			value=f'Has been changed to {nickname}'
		)
		await member.edit(nick=nickname)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(FunCommands(bot))
