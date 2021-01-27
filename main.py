import discord
from discord.ext import commands, tasks
import asyncio
import json
import datetime
import uuid
import database
from log import log
from configcreator import Config
import sys
import traceback
import csv
import time
import os

intents = discord.Intents.default()
intents.members = True
intents.presences = True
# We put here the name of all the bot extensions
extensions = ['cogs.profilecommands', 'cogs.databasecommands', 'cogs.infocommands', 'cogs.step', 'cogs.misc']

# Creating the folder path to load folders
#folderpath = "\\".join(__file__.split("\\")[:-1])+"\\"
#if folderpath == "\\":
#	folderpath = "/".join(__file__.split("/")[:-1])+"/"
#if folderpath =="/":
#	folderpath =""


config = Config()

# Creating the bot object and removing the default help command
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.prefix), description=config.description, intents=intents)
bot.remove_command('help')

# loading the cogs extensions
if __name__ == '__main__':
	print("--------------")
	for ext in extensions :
		bot.load_extension(ext)
		log(f"successfully loaded extension {ext}")
	bot.load_extension("jishaku")
	log("successfully loaded jishaku")
	


@bot.event  # when the bot is connected and ready to run commands.
async def on_ready():
	print('--------------')
	log(f"{config.description}")
	log('Logged in successfully !')
	log(f"Bot username : {bot.user.name}")
	log(f"Bot id : {bot.user.id}")
	await bot.change_presence(activity=discord.Game(name=f"{config.prefix}help | {len(bot.users)} users on {len(bot.guilds)} guilds."))
	print('--------------')
	log("LOADING COMPLETE. BOT CAN NOW BE USED.")
	print("--------------")

	bot.cogs["DatabaseCog"].energy.start() # launching energy recovering loop from DatabaseCog cog
	log("Energy recovery loop started !")
	activity.start() # launching automatic activity update
	log("Actity update loop started !")


@bot.event
async def on_command_error(ctx, error):

	if hasattr(ctx.command, 'on_error'):
		return

	if isinstance(error, commands.CommandNotFound):
		log(f"{ctx.author} tried to invoke the command '{ctx.message.content}' but this command is unknown")
	else:
		# All other Errors not returned come here. And we can just print the default TraceBack.
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)







@bot.command(name="ping", aliases=["pong"], description = "A simple command that pings the bot to check if he is awake.")
async def ping(ctx):
	"""A simple command that pings the bot to check if he is awake."""
	
	start = time.perf_counter()
	
	embed = discord.Embed(title="PONG :ping_pong: ", description="I'm online ! :signal_strength:", colour=config.colour, timestamp=datetime.datetime.utcnow())
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.set_footer(text=bot.user.name + ' - requested by ' + str(ctx.author), icon_url=ctx.author.avatar_url)
	message = await ctx.send(embed=embed)
	
	end = time.perf_counter()
	duration = (end-start)*1000
	embed.add_field(name="Latency", value = "{:.2f}ms".format(duration), inline = False)
	await message.edit(embed=embed)
	log(f"{ctx.author} pinged the bot.")


@bot.command(name="say", aliases=['tell', 'repeat'], description = '[ADMIN] Make the bot say something')
async def say(ctx, *content):
	if ctx.author.id in config.admins :
		message = await ctx.send(' '.join(content))
		await ctx.message.delete()
		log(f"{ctx.author} made the bot say '{' '.join(content)}'")
	else : 
		await ctx.send("I'm sorry, this command is for admins only.")


@tasks.loop(seconds=1200.0)
async def activity():
	activityString = f"{config.prefix}help | {len(bot.users)} users on {len(bot.guilds)} guilds."
	log(f"[LOOP] Updated activity : {activityString}")
	await bot.change_presence(activity=discord.Game(name=activityString))

	stats = [int(datetime.datetime.utcnow().timestamp()), len(bot.users), len(bot.guilds), database.get_player_number(), len(bot.cogs), len(bot.commands)]
	with open("stats.csv",encoding='utf-8' , mode="a", newline='') as f:
		writer = csv.writer(f)
		writer.writerow(stats)
		log("[STATS] Uploaded stats to csv file")




# runs the bot
bot.run(config.token, bot=True, reconnect=True)
print("FATAL ERROR ! THE CONNEXION TO THE BOT HAS BEEN TERMINATED. THE BOT CANNOT INTERACT WITH DISCORD ANYMORE. PLEASE REBOOT.")
