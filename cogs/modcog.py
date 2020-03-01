from discord.ext import commands
import discord


class ModCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def ban(self, ctx, member: discord.Member, *, reason=None):
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

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def unban(self, ctx, *, member):
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

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def kick(self, ctx, member: discord.Member, *, reason=None):
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

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def mute(self, ctx, member: discord.Member = None):
		if not member:
			await ctx.send('Please enter a member')
			return
		role = discord.utils.get(ctx.guild.roles, name='muted')
		await member.add_roles(role)
		await ctx.send(f'@{member} has been muted by @{ctx.author}')

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def unmute(self, ctx, member: discord.Member = None):
		if not member:
			await ctx.send('Please enter a member')
			return
		role = discord.utils.get(ctx.guild.roles, name='muted')
		await member.remove_roles(role)
		await ctx.send(f'@{member} has been unmuted by @{ctx.author}')

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def add_mod(self, ctx, member: discord.Member = None):
		role = discord.utils.get(ctx.guild.roles, name='Admin')
		await member.add_roles(role)
		await ctx.send(f'{member} has been promoted to admin by: {ctx.author}')

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def minus_mod(self, ctx, member: discord.Member = None):
		role = discord.utils.get(ctx.guild.roles, name='Admin')
		await member.remove_roles(role)
		await ctx.send(f'{member} has had admin role removed by: {ctx.author}')

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def warn(self, ctx, member: discord.Member = None, *, reason=None):
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

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def give_role(self, ctx, role: str, member: discord.Member = None):
		r = discord.utils.get(ctx.guild.roles, name=role)
		await member.add_roles(r)
		await ctx.send(f'Added {role} role to {member}')


def setup(bot):
	bot.add_cog(ModCommands(bot))
