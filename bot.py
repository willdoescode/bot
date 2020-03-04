from configparser import (
	ConfigParser
)
from discord.ext import (
	commands,
)
config = ConfigParser()
config.read('configs.ini')
client = commands.Bot(command_prefix='%')
client.remove_command('help')
extensions = [
	'cogs.errorcatch',
	'cogs.webscraping',
	'cogs.funcogs',
	'cogs.modcog',
	'cogs.events',
	'cogs.helpcog',
	'cogs.chatmanage',
	'cogs.math'
]
if __name__ == '__main__':
	for ext in extensions:
		try:
			client.load_extension(ext)
			print(f'Loaded {ext}')
		except:
			print(f'{ext} Failed to load')

client.run(config['discord']['key'])
