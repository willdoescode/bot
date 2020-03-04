from discord.ext import commands
import discord
import requests
import random


class FunCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.responses = responses = [
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
		self.jokes = jokes = [
			'Light travels faster than sound. That\'s why some people appear bright until you hear them '
			'speak',
			'I was wondering why the ball was getting bigger. Then it hit me',
			'I have a few jokes about unemployed people, but none of them work',
			'"I have a split personality," said Tom, being frank.',
			'When life gives you melons, you\'re dyslexic',
			'How do you make holy water? You boil the hell out of it',
			'I Renamed my iPod The Titanic, so when I plug it in, it says “The Titanic is syncing.”',
			'Will glass coffins be a success? Remains to be seen',
			'It\'s hard to explain puns to kleptomaniacs because they always take things literally',
			'Last night, I dreamed I was swimming in an ocean of orange soda. But it was just a Fanta sea',
			'I lost my job at the bank on my very first day. A woman asked me to check her balance, '
			'so I pushed her over',
			'What’s the difference between a hippo and a zippo? One is really heavy and the other is a '
			'little lighter',
			'Two windmills are standing in a wind farm. One asks, “What’s your favorite kind of music?” '
			'The other says, “I’m a big metal fan.”',
			'Did you hear about the guy whose whole left side was cut off? He’s all right now',
			'Hear about the new restaurant called Karma? There’s no menu - you get what you deserve',
			'England doesn\'t have a kidney bank, but it does have a Liverpool',
			'A cross-eyed teacher couldn’t control his pupils',
			'Is it ignorance or apathy that\'s destroying the world today? I don\'t know and don\'t '
			'really '
			'care',
			'How do you throw a space party? You planet'
		]

	@commands.command()
	async def pun(self, ctx):
		joke = random.choice(self.jokes)
		embed = discord.Embed(
			color=discord.Color.green()
		)
		embed.add_field(
			name='Joke',
			value=f'{joke}',
			inline=False
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def expand(self, ctx, link):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		if 'bit.ly' in link:
			embed.add_field(name=f'Link: {link}', value=f'Expanded: {requests.get(link).url}',
			                inline=True)
			await ctx.send(embed=embed)
		else:
			await ctx.send('Please enter a valid bit.ly link')

	@commands.command()
	async def coinflip(self, ctx):
		embed = discord.Embed(
			color=discord.Color.purple()
		)
		ok = ['heads', 'tails']
		embed.add_field(
			name='Coin Says:',
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
			color=discord.Color.dark_red()
		)
		show_avatar.set_image(
			url=member.avatar_url
		)
		show_avatar.add_field(
			name=member.display_name,
			value='Avatar',
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
			color=discord.Color.purple()
		)
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
			color=discord.Color.red()
		)
		embed.add_field(
			name=name,
			value=f'joined: {joined}\nstatus: {status}\nactivity: {activity}\nroles: '
			      f'{roles}\nguild: {guild}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command(aliases=['embed'])
	@commands.has_permissions(manage_messages=True)
	async def em(self, ctx, *, message: str):
		embed = discord.Embed(
			color=discord.Color.green()
		)
		embed.add_field(name=ctx.author, value=message, inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	async def nick(self, ctx, *, nickname: str):
		await self.bot.change_nickname(ctx.author, nickname=nickname)
		await ctx.send('Changed nick')
def setup(bot):
	bot.add_cog(FunCommands(bot))
