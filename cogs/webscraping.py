from discord.ext import commands
import discord
from PyDictionary import PyDictionary
import praw
from configparser import ConfigParser
import tweepy
from imgurpython import ImgurClient
import time
import random

config = ConfigParser()
config.read('configs.ini')


class WebScraping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.dictionary = PyDictionary
		self.reddit = praw.Reddit(
			client_id=config['reddit']['client_id'],
			client_secret=config['reddit']['client_secret'],
			user_agent=config['reddit']['user_agent']
		)
		self.shower_thoughts = self.reddit.subreddit('Showerthoughts')
		self.imgur_bot = ImgurClient(
			config['imgur']['consumer_key'],
			config['imgur']['consumer_secret']
		)
		self.auth = tweepy.OAuthHandler(
			config['twitter']['consumer_key'],
			config['twitter']['consumer_secret']
		)
		self.auth.set_access_token(
			config['twitter']['access_key'],
			config['twitter']['access_secret']
		)
		self.api = tweepy.API(self.auth)

	@commands.command()
	async def define(self, ctx, word: str):
		mean = self.dictionary.meaning(word)
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Definition', icon_url=self.bot.user.avatar_url)
		for name, value in mean.items():
			embed.add_field(name=name, value=value, inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	async def showerthought(self, ctx, rank='hot', value: int = 1):
		embed = discord.Embed(
			color=discord.Color.dark_orange(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Showerthought', icon_url=self.bot.user.avatar_url)
		count = 1
		if value < 10:
			if rank == 'new':
				for sub in self.shower_thoughts.new(limit=value):
					if not sub.stickied:
						embed.add_field(
							name=f'{count}:',
							value=f'{sub.title}\n{sub.url}',
							inline=True
						)
						count += 1
			elif rank == 'top':
				for sub in self.shower_thoughts.top(limit=value):
					if not sub.stickied:
						embed.add_field(
							name=f'{count}:',
							value=f'{sub.title}\n{sub.url}',
							inline=True
						)
						count += 1
			elif rank == 'hot':
				for sub in self.shower_thoughts.hot(limit=value + 2):
					if not sub.stickied:
						embed.add_field(
							name=f'{count}:',
							value=f'{sub.title}\n{sub.url}',
							inline=True
						)
						count += 1
			elif rank == 'controversial':
				for sub in self.shower_thoughts.controversial(limit=value):
					if not sub.stickied:
						embed.add_field(
							name=f'{count}:',
							value=f'{sub.title}\n{sub.url}',
							inline=True
						)
						count += 1
			elif rank == 'rising':
				for sub in self.shower_thoughts.rising(limit=value):
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

	@commands.command()
	async def imgur(self, ctx):
		front_page = self.imgur_bot.gallery()
		embed = discord.Embed(
			color=discord.Color.orange(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Imgur', icon_url=self.bot.user.avatar_url)
		count = 1
		for item in front_page:
			embed.add_field(name=f'{count}', value=f'{item.link}\nviewed {item.views} times',
			                inline=True)
			count += 1
			if count >= 4:
				await ctx.send(embed=embed)
				break

	@commands.command()
	async def getreddit(self, ctx, sub='teenagers', rank='top', value=1):
		subreddit = self.reddit.subreddit(str(sub))
		embed = discord.Embed(
			color=discord.Color.dark_green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Reddit', icon_url=self.bot.user.avatar_url)
		count = 1
		if rank == 'top':
			for post in subreddit.top(limit=value):
				embed.add_field(
					name=f'{count}: {post.title}',
					value=f'{post.url}\n{post.id}{post.score} upvotes: {post.ups} downvotes '
					      f'{post.downs}',
					inline=True
				)
				count += 1
			await ctx.send(embed=embed)
		elif rank == 'hot':
			for post in subreddit.hot(limit=value):
				embed.add_field(
					name=f'{count}: {post.title}',
					value=f'{post.url}\n{post.id}{post.score} upvotes: {post.ups} down'
					      f'votes {post.downs}',
					inline=True
				)
				count += 1
			await ctx.send(embed=embed)
		if rank == 'new':
			for post in subreddit.new(limit=value):
				embed.add_field(
					name=f'{count}: {post.title}',
					value=f'{post.url}\n{post.id}{post.score} upvotes: {post.ups} down'
					      f'votes {post.downs}',
					inline=True
				)
				count += 1
			await ctx.send(embed=embed)

	@commands.command()
	async def trending(self, ctx, hashtag: str = 'cool', value: int = 1):
		search_hashtag = tweepy.Cursor(self.api.search, q=f'{hashtag}').items(value)
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Trending Tweets', icon_url=self.bot.user.avatar_url)
		count = 1
		for tweet in search_hashtag:
			x = tweet.id
			y = self.api.get_status(x)
			a = y.author
			embed.add_field(
				name=f'{count}: @{a.screen_name}',
				value=f'{tweet.text}\nhttps://twitter.com/{tweet.user.screen_name}/status/'
				      f'{tweet.id}',
				inline=True
			)
			count += 1
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(WebScraping(bot))
