from discord.ext import commands
import discord


class Math(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def add(self, ctx, a: int, b: int):
		await ctx.send(f'{a} + {b} = {a + b}')

	@commands.command()
	async def subtract(self, ctx, a: int, b: int):
		await ctx.send(f'{a} - {b} = {a - b}')

	@commands.command()
	async def multiply(self, ctx, a: int, b: int):
		await ctx.send(f'{a} * {b} = {a * b}')

	@commands.command()
	async def divide(self, ctx, a: int, b: int):
		if b == 0:
			await ctx.send('don\'t divide by zero')
		else:
			await ctx.send(f'{a} / {b} = {a / b}')


def setup(bot):
	bot.add_cog(Math(bot))
