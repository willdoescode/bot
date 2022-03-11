from configparser import (
	ConfigParser
)
from discord.ext import (
	commands,
)
import discord
import os
import sys
config = ConfigParser()
config.read('configs.ini')
client = commands.Bot(command_prefix=commands.when_mentioned_or('.'),intents=discord.Intents.all(),help_command=None,case_insensitive=True)



## TODO Set the id in the check of reload to the id of the owner


if __name__ == '__main__':
	for file in os.listdir('cogs'):
		if file.endswith('.py'):
			try:
				print(f"Loading {file}")
				client.load_extension(f'cogs.{file[:-3]}')
			except Exception as e:
				print(e,file=sys.stderr)
			

	@client.command()
	@commands.check(lambda x: x.author.id==1234567890)
	async def reload(ctx):
		for extension in client.cogs.keys():
			try:
				
				await ctx.send(f'Reloading {extension}')
				client.reload_extension(extension)
			except:
				await ctx.send(f'failed to reload {extension} extension')
		

client.run(config['discord']['key'])
