from discord.ext import commands, tasks
import discord
import json
import asyncio


class Level(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.loop.create_task(self.save_users())

		with open('users.json', 'r') as f:
			self.users = json.load(f)

	async def save_users(self):
		await self.bot.wait_until_ready()
		while not self.bot.is_closed():
			with open('users.json', 'w') as f:
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
		if not member:
			value = f"{self.users[str(ctx.author.id)]['level']}/" \
			        f"{4 * (self.users[str(ctx.author.id)] ** 3) / 5}"
			icon_url = ctx.author.avatar_url
			member_id = str(ctx.author.id)
		else:
			value = f"{self.users[member_id]['level']}/" \
			        f"{4 * (self.users[member_id] ** 3) / 5}"
			icon_url = member.avatar_url

		if member_id not in self.users:
			await ctx.send('Member doesnt have a level')

		elif member_id in self.users:
			em = discord.Embed(
				color=member.color,
				timestamp=ctx.message.created_at
			)
			em.set_author(name=f'Level - {member}', icon_url=icon_url)
			em.add_field(name="Level", value=self.users[member_id]['level'] - 1)
			em.add_field(
				name="XP",
				value=value
			)
			await ctx.send(embed=em)


def setup(bot):
	bot.add_cog(Level(bot))
