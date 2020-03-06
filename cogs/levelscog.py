from discord.ext import commands
import discord
import json
import asyncio


class Level(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.loop.create_task(self.save_users())

		with open('jsonfiles.users', 'r') as f:
			self.users = json.load(f)

	async def save_users(self):
		await self.bot.wait_until_ready()
		while not self.bot.is_closed():
			with open('jsonfiles.users', 'w') as f:
				json.dump(self.users, f, indent=4)

			await asyncio.sleep(5)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		author_id = str(message.author.id)

		if author_id not in self.users:
			self.users[author_id] = {}
			self.users[author_id]['level'] = 1
			self.users[author_id]['exp'] = 0

		self.users[author_id]['exp'] += 1

		if self.users[author_id]['exp'] >= round(4 * (self.users[author_id]['level'] ** 3) / 5):
			await message.channel.send(f"{message.author.mention} is now level"
			               f" {self.users[author_id]['level']}")
			self.users[author_id]['level'] += 1

	@commands.command()
	async def level(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if member_id not in self.users:
			await ctx.send('Member doesnt have a level')
		else:
			embed = discord.Embed(
				color=member.color,
				timestamp=ctx.message.created_at
			)
			embed.set_author(name=f'Level - {member}', icon_url=self.bot.user.avatar_url)
			embed.add_field(name="Level", value=self.users[member_id]['level'] - 1)
			embed.add_field(name="XP", value=self.users[member_id]['exp'])

			await ctx.send(embed=embed)

	@commands.command(aliases=['lb'])
	async def leaderboard(self, ctx):
		embed = discord.Embed(
			color=discord.Color.purple(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='ScoreBoard', icon_url=self.bot.user.avatar_url)
		count = 0
		for ids in self.users:
			count += 1
			name = self.bot.get_user(int(ids))
			embed.add_field(
				name=f'{count}: {name}',
				value=f"Level: {self.users[ids]['level'] - 1}",
				inline=True
			)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Level(bot))
