import discord
from imgurpython import ImgurClient
from PyDictionary import PyDictionary
import tweepy
import requests
import json
import random
import praw
from itertools import cycle
from configparser import (
	ConfigParser
)
from discord.ext import (
	commands,
	tasks,
)

config = ConfigParser()

dictionary = PyDictionary()

config.read('twitterkeys.ini')

CONSUMER_KEY = config['keys']['consumer_key']
consumer_secret = config['keys']['consumer_secret']

access_token = config['tokens']['access_token']
access_token_secret = config['tokens']['access_secret']

auth = tweepy.OAuthHandler(
	CONSUMER_KEY,
	consumer_secret
)
auth.set_access_token(
	access_token,
	access_token_secret
)

api = tweepy.API(auth)

config.read('imbotkeys.ini')

imbot = ImgurClient(
	config['keys']['consumer_key'],
	config['keys']['consumer_secret']
)

config.read('redditkeys.ini')

reddit = praw.Reddit(
	client_id=config['ids']['client_id'],
	client_secret=config['ids']['client_secret'],
	user_agent=config['agent']['user_agent']
)

reddit.read_only = True

shower_thoughts = reddit.subreddit('Showerthoughts')

client = commands.Bot(command_prefix='.')

client.remove_command('help')

status = cycle(['with your toys', 'with a dog', ' a guitar', 'csgo',
                'with fire', 'with your feeling', 'on my own', 'a song',
                'with bot things', 'oil changing simulator'])

jokes = [
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


@tasks.loop(seconds=1)
async def big_loop():
	await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_ready():
	embed = discord.Embed(
		color=discord.Color.dark_green()
	)
	channel = discord.utils.get(client.get_all_channels(), name='logs')
	embed.add_field(
		name=f'{client.user.name}',
		value='Has connected to the server'
	)
	big_loop.start()
	await channel.send(embed=embed)
	print(f'{client.user.name} bot has connected to discord')


@client.command()
async def ping(ctx):
	await ctx.send(f'{round(client.latency * 1000)}ms')


responses = [
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



@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
	embed = discord.Embed(
		color=discord.Color.purple()
	)
	embed.add_field(
		name=f'{ctx.author} has asked: {question}',
		value=f'Answer: {random.choice(responses)}',
		inline=True
	)
	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=100000):
	await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	embed = discord.Embed(
		color=discord.Color.red()
	)
	await member.kick(reason=reason)
	embed.add_field(
		name=f'{member}',
		value=f'has been kicked for: {reason} by: {ctx.author}',
		inline=True
	)
	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	embed = discord.Embed(
		color=discord.Color.dark_red()
	)
	await member.ban(reason=reason)
	embed.add_field(
		name=f'{member}',
		value=f'Has been banned for: {reason} by: {ctx.author}',
		inline=True
	)
	await ctx.send(embed=embed)


# ^ checks if user has admin perms, then allows for banning of other users


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
	embed = discord.Embed(
		color=discord.Color.green()
	)
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			embed.add_field(
				name=f'{user.name}',
				value=f'has been unbanned by: {ctx.author}',
				inline=True
			)
			await ctx.send(embed=embed)
			return


@client.event
async def on_member_join(ctx, member: discord.Member):
	embed = discord.Embed(
		color=discord.Color.green()
	)
	channel = discord.utils.get(client.get_all_channels(), name='joins-and-leaves')
	embed.add_field(
		name='Welcome to the server:',
		value=f'@{member}',
		inline=False
	)
	await channel.send(embed=embed)
	role = discord.utils.get(ctx.guild.roles, name='new player')
	await member.add_roles(role)


@client.event
async def on_member_remove(member):
	channel = client.get_channel(678468548775116852)
	await channel.send(f'Sad to see you go @{member}')


@client.event
async def on_command_error(ctx, error):
	me = '371457814775857152'
	if isinstance(error, commands.CommandNotFound):
		await ctx.send('Invalid command')
	elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
		await ctx.send('Invalid Permissions')
	elif isinstance(error, discord.ext.commands.errors.BadArgument):
		await ctx.send('Please use the commands properly, dm @PieTales#0495 if you need help')
	elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send('Please finish the command')
	elif isinstance(error, RuntimeError):
		await ctx.send('please enter your command correctly')
	elif isinstance(error, RuntimeWarning):
		await ctx.send('Coder is Stupid and Forgot to Await Something in the code')


@client.command()
async def dm(ctx):
	await ctx.author.send('I done slid into your dms')
	await ctx.send(f'sliding into {ctx.author}\'s dms')


@client.command()
async def help(ctx):

	with open('help.json') as f:
		help_commands = json.load(f)

	with open('help2.json') as f:
		help2_commands = json.load(f)

	alsoembed = discord.Embed(
		color=discord.Color.orange()
	)

	embed = discord.Embed(
		color=discord.Color.orange()
	)

	embed.set_author(
		name='Help is here'
	)

	for name, value in help_commands.items():
		embed.add_field(name=name, value=value, inline=True)

	for names, values in help2_commands.items():
		alsoembed.add_field(name=names, value=values, inline=True)

	await ctx.send(embed=embed)
	await ctx.send(embed=alsoembed)


@client.command()
async def pun(ctx):
	joke = random.choice(jokes)
	embed = discord.Embed(
		color=discord.Color.green()
	)
	embed.add_field(
		name='Joke',
		value=f'{joke}',
		inline=False
	)
	await ctx.send(embed=embed)


@client.command()
async def show_code(ctx):
	await ctx.author.send('https://i.imgur.com/qIKR0Qt.gif lol you thought')


@client.command(aliases=['pfp'])
async def avatar(ctx, member: discord.Member):
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


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None):
	if not member:
		await ctx.send('Please enter a member')
		return
	role = discord.utils.get(ctx.guild.roles, name='muted')
	await member.add_roles(role)
	await ctx.send(f'@{member} has been muted by @{ctx.author}')


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
	if not member:
		await ctx.send('Please enter a member')
		return
	role = discord.utils.get(ctx.guild.roles, name='muted')
	await member.remove_roles(role)
	await ctx.send(f'@{member} has been unmuted by @{ctx.author}')


@client.command()
async def coinflip(ctx):
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


@client.command()
@commands.has_permissions(administrator=True)
async def add_mod(ctx, member: discord.Member = None):
	role = discord.utils.get(ctx.guild.roles, name='Admin')
	await member.add_roles(role)
	await ctx.send(f'{member} has been promoted to admin by: {ctx.author}')


@client.command()
@commands.has_permissions(administrator=True)
async def minus_mod(ctx, member: discord.Member = None):
	role = discord.utils.get(ctx.guild.roles, name='Admin')
	await member.remove_roles(role)
	await ctx.send(f'{member} has had admin role removed by: {ctx.author}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def yell(ctx, *, message=None):
	await ctx.send(f'@everyone {message}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def yell_here(ctx, *, message=None):
	await ctx.send(f'@here {message}')


@client.command()
async def add(ctx, a: int, b: int):
	await ctx.send(f'{a} + {b} = {a + b}')


@client.command()
async def subtract(ctx, a: int, b: int):
	await ctx.send(f'{a} - {b} = {a - b}')


@client.command()
async def multiply(ctx, a: int, b: int):
	await ctx.send(f'{a} * {b} = {a * b}')


@client.command()
async def divide(ctx, a: int, b: int):
	if b == 0:
		await ctx.send('don\'t divide by zero')
	else:
		await ctx.send(f'{a} / {b} = {a / b}')


@client.command()
async def showerthought(ctx, rank='hot', value: int = 1):
	embed = discord.Embed(
		color=discord.Color.dark_orange()
	)
	count = 1
	if value < 10:
		if rank == 'new':
			for sub in shower_thoughts.new(limit=value):
				if not sub.stickied:
					embed.add_field(
						name=f'{count}:',
						value=f'{sub.title}\n{sub.url}',
						inline=True
					)
					count += 1
		elif rank == 'top':
			for sub in shower_thoughts.top(limit=value):
				if not sub.stickied:
					embed.add_field(
						name=f'{count}:',
						value=f'{sub.title}\n{sub.url}',
						inline=True
					)
					count += 1
		elif rank == 'hot':
			for sub in shower_thoughts.hot(limit=value + 2):
				if not sub.stickied:
					embed.add_field(
						name=f'{count}:',
						value=f'{sub.title}\n{sub.url}',
						inline=True
					)
					count += 1
		elif rank == 'controversial':
			for sub in shower_thoughts.controversial(limit=value):
				if not sub.stickied:
					embed.add_field(
						name=f'{count}:',
						value=f'{sub.title}\n{sub.url}',
						inline=True
					)
					count += 1
		elif rank == 'rising':
			for sub in shower_thoughts.rising(limit=value):
				if not sub.stickied:
					embed.add_field(
						name=f'{count}:',
						value=f'{sub.title}\n{sub.url}',
						inline=True
					)
					count += 1
		await ctx.send(embed=embed)
	else:
		await ctx.send('Please choose a lower number')


@client.command()
async def getreddit(ctx, sub='teenagers', rank='top', value=1):
	subreddit = reddit.subreddit(str(sub))
	embed = discord.Embed(
		color=discord.Color.dark_green()
	)
	count = 1
	if rank == 'top':
		for post in subreddit.top(limit=value):
			embed.add_field(
				name=f'{count}: {post.title}',
				value=f'{post.url}{post.id}{post.score} upvotes: {post.ups} downvotes '
				      f'{post.downs}',
				inline=True
			)
			count += 1
		await ctx.send(embed=embed)
	elif rank == 'hot':
		for post in subreddit.hot(limit=value):
			embed.add_field(
				name=f'{count}: {post.title}',
				value=f'{post.url}{post.id}{post.score} upvotes: {post.ups} down'
				      f'votes {post.downs}',
				inline=True
			)
			count += 1
		await ctx.send(embed=embed)
	if rank == 'new':
		for post in subreddit.new(limit=value):
			embed.add_field(
				name=f'{count}: {post.title}',
				value=f'{post.url}{post.id}{post.score} upvotes: {post.ups} down'
				      f'votes {post.downs}',
				inline=True
			)
			count += 1
		await ctx.send(embed=embed)


@client.command()
async def imgur(ctx):
	front_page = imbot.gallery()
	embed = discord.Embed(
		color=discord.Color.orange()
	)
	count = 1
	for item in front_page:
		embed.add_field(name=f'{count}', value=f'{item.link}\nviewed {item.views} times',
		                inline=True)
		count += 1
		if count >= 4:
			await ctx.send(embed=embed)
			break


@client.command()
async def trending(ctx, hashtag: str = 'cool', value: int = 1):
	search_hashtag = tweepy.Cursor(api.search, q=f'{hashtag}').items(value)
	embed = discord.Embed(
		color=discord.Color.green()
	)
	count = 1
	for tweet in search_hashtag:
		x = tweet.id
		y = api.get_status(x)
		a = y.author
		embed.add_field(
			name=f'{count}: @{a.screen_name}',
			value=f'{tweet.text}\nhttps://twitter.com/{tweet.user.screen_name}/status/{tweet.id}',
			inline=True
		)
		count += 1
	await ctx.send(embed=embed)


@client.command()
async def expand(ctx, link):
	embed = discord.Embed(
		color=discord.Color.green()
	)
	if 'bit.ly' in link:
		embed.add_field(name=f'Link: {link}', value=f'Expanded: {requests.get(link).url}',
		                inline=True)
		await ctx.send(embed=embed)
	else:
		await ctx.send('Please enter a valid bit.ly link')


@client.command()
async def define(ctx, word: str):
	mean = dictionary.meaning(word)
	embed = discord.Embed(
		color=discord.Color.green()
	)
	for key, value in mean.items():
		embed.add_field(name=f'{key}', value=f'{value}', inline=True)
	await ctx.send(embed=embed)


@client.command()
async def synonym(ctx, word):
	embed = discord.Embed(
		color=discord.Color.green()
	)
	syn = dictionary.synonym(word)
	for key, value in syn.items():
		embed.add_field(
			name=f'{key}',
			value=f'{value}',
			inline=True
		)
	await ctx.send(embed=embed)


@client.command()
async def antonym(ctx, word):
	embed = discord.Embed(
		color=discord.Color.green()
	)
	syn = dictionary.antonym(word)
	for key, value in syn.items():
		embed.add_field(
			name=f'{key}',
			value=f'{value}',
			inline=True
		)
	await ctx.send(embed=embed)


@client.command()
async def members(ctx):
	embed = discord.Embed(
		color=discord.Color.green()
	)
	member = list(client.get_all_members())
	embed.add_field(
		name='Amount of members:',
		value=f'{len(member)}',
		inline=True
	)
	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member = None, *, reason=None):
	embed = discord.Embed(
		color=discord.Color.red()
	)
	embed.add_field(
		name='WARNING',
		value=f'@{member} has been warned for: {reason}',
		inline=True
	)
	await member.send(embed=embed)
	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def give_role(ctx, role: str, member: discord.Member = None):
	r = discord.utils.get(ctx.guild.roles, name=role)
	await member.add_roles(r)
	await ctx.send(f'Added {role} role to {member}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def cmessage(ctx, channel: discord.TextChannel = None):
	channel = channel or ctx.channel
	count = 0
	async for _ in channel.history(limit=None):
		count += 1
	await ctx.send(f'There are {count} messages in {channel.mention}')


config.read('discordkey.ini')
client.run(config['keys']['key'])
