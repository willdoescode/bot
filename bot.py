from configparser import (
	ConfigParser
)
from discord.ext import (
	commands,
)
config = ConfigParser()
config.read('configs.ini')
client = commands.Bot(command_prefix='.')
client.remove_command('help')
extensions = [
	'cogs.errorcatch',
	'cogs.webscraping',
	'cogs.funcogs',
	'cogs.modcog',
	'cogs.events',
	'cogs.helpcog',
	'cogs.chatmanage',
	'cogs.levelscog',
	'cogs.math',
	'cogs.comscog'
]
if __name__ == '__main__':
	for ext in extensions:
		client.load_extension(ext)
		print(f'Loaded {ext}')

	@client.command()
	@commands.has_permissions(administrator=True)
	async def reload(ctx):
		for extension in extensions:
			try:
				client.unload_extension(extension)
				await ctx.send(f'Reloading {extension}')
				client.load_extension(extension)
			except:
				await ctx.send(f'failed to reload {extension} extension')

client.run(config['discord']['key'])
