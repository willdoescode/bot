from discord.ext import commands
import discord


class ModCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def ban(self, ctx, member: discord.Member, *, reason=None):
		embed = discord.Embed(
			color=discord.Color.dark_red(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Banned', icon_url=self.bot.user.avatar_url)
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
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Unban', icon_url=self.bot.user.avatar_url)
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
			color=discord.Color.red(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Kicked', icon_url=self.bot.user.avatar_url)
		await member.kick(reason=reason)
		embed.add_field(
			name=f'{member.display_name}',
			value=f'has been kicked for: {reason} by: {ctx.author}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def mute(self, ctx, member: discord.Member = None, *, reason: str = None):
		role = discord.utils.get(ctx.guild.roles, name='muted')
		await member.add_roles(role)
		embed = discord.Embed(
			color=discord.Color.red(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Muting', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=f'{member.display_name}',
			value=f'has been muted by {ctx.author} for {reason}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def unmute(self, ctx, member: discord.Member = None):
		role = discord.utils.get(ctx.guild.roles, name='muted')
		await member.remove_roles(role)
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Unmuting', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=f'{member.display_name}',
			value=f'has been unmuted by {ctx.author}',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command(aliases=['+role'])
	@commands.has_permissions(administrator=True)
	async def giverole(self, ctx, role=None, member: discord.Member = None):
		roles = discord.utils.get(ctx.guild.roles, name=role)
		embed = discord.Embed(
			color=discord.Color.green(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Role Adding', icon_url=self.bot.user.avatar_url)
		await member.add_roles(roles)
		embed.add_field(
			name=f'{member.display_name}',
			value=f'has been given the {roles} role',
			inline=True
		)
		await ctx.send(embed=embed)

	@commands.command(aliases=['-role'])
	@commands.has_permissions(administrator=True)
	async def removerole(self, ctx,  role=None, member: discord.Member = None):
		roles = discord.utils.get(ctx.guild.roles, name=role)
		await member.remove_roles(roles)
		embed = discord.Embed(
			color=discord.Color.red(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='Role Removal', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=f'{member.display_name}',
			value=f'Has had {roles} role removed'
		)
		await ctx.send(embed=embed)

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
			color=discord.Color.red(),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name='WARNING', icon_url=self.bot.user.avatar_url)
		embed.add_field(
			name=' .',
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
