import discord
from discord.ext import commands
import asyncio
from log import log
import database
from configcreator import Config
import datetime
import psutil
import os
import platform
import sys

config = Config()

class InfoCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name="info", aliases = ["i", "uptime", "stats"], description = "Retrieves informations about the bot and the server running it")
	async def info(self, ctx):
		uptime = int(datetime.datetime.now().timestamp() - config.boottime)
		min, sec = divmod(uptime, 60)
		hours, min = divmod(min, 60)
		embed = discord.Embed(title=f"Informations about the bot :", description="", colour=config.colour, timestamp=datetime.datetime.utcnow())
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
		embed.add_field(name="System Info :", value = f"""OS : `{platform.platform()}`
		Python Version : `{sys.version}`
		Bot uptime : `{int(hours)}h{int(min)}m{int(sec)}s`
		""", inline = False)
		embed.add_field(name="Performance :", value = f"""System CPU usage : `{psutil.cpu_percent()}`%
		System RAM usage : `{round(psutil.virtual_memory().used / (1024.0**3),2)}`GB/`{round(psutil.virtual_memory().total / (1024.0**3),2)}`GB (`{psutil.virtual_memory()[2]}`%)
		RAM used by the program : `{round(psutil.Process(os.getpid()).memory_info()[0] / (1024.0**3),2)}`GB
		Disk usage : `{round(psutil.disk_usage('/').used / (1024.0**3),2)}`GB/`{round(psutil.disk_usage('/').total / (1024.0**3),2)}`GB (`{psutil.disk_usage('/').percent}`%)
		""", inline = False)
		embed.add_field(name="Bot Info :", value = f"""Commands count : `{len(self.bot.commands)}`
		Cogs count : `{len(self.bot.cogs)}`
		Guilds count : `{len(self.bot.guilds)}`
		Users count : `{len(self.bot.users)}`
		Players count : `{database.get_player_number()}`
		""", inline=False)
		embed.add_field(name="Links :", value = f"[Invite me on your server](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=379969)", inline = False)
		await ctx.send(embed=embed)
		log(f"{ctx.author} asked for infos about the bot.")
	
	@commands.command(name="help", description="Returns all commands available")
	async def help(self,ctx):
		log(f"{ctx.author} asked for help about the bot")
		helptext = "Commands list :```"
		for command in self.bot.commands:
			helptext+=f"{command} : {command.description}\n"
		helptext+="```"
		helptext+="Cogs list :```\n"
		helptext+= "\n".join([cog for cog in self.bot.cogs])
		helptext+="```"
		await ctx.send(helptext)
		helptext+= "WARNING : this help command is temporary."
	
	@commands.command(name="users", description="Prints to the console all the users the bot can see")
	async def users(self, ctx):
		await ctx.send("Check your console : the user list has been printed")
		for i in self.bot.users:
			print(i)
	



def setup(bot):
	bot.add_cog(InfoCog(bot))
