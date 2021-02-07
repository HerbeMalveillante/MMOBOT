# commands that display infos about the bot.

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
import matplotlib.pyplot as plt
import csv
import datetime
from io import BytesIO

config = Config()

class InfoCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name="info", aliases = ["i", "uptime", "stats", "invite", "link", "links"], description = "Retrieves informations about the bot and the server running it")
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
		embed.add_field(name="Links :", value = f"""
		[Invite me on your server](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=379969)
		[Official support server](https://discord.gg/vRA4gdraaC)
		[GitHub repo](https://github.com/HerbeMalveillante/MMOBOT)
		""", inline = False)
		await ctx.send(embed=embed)
		log(f"{ctx.author} asked for infos about the bot.")
	
	@commands.command(name="help", description="Returns all commands available")
	async def help(self,ctx):
		log(f"{ctx.author} asked for help about the bot")
		#helptext = "Commands list :```"
		#for command in self.bot.commands:
		#	helptext+=f"{command} : {command.description}\n"
		#helptext+="```"
		#helptext+="Cogs list :```\n"
		#helptext+= "\n".join([cog for cog in self.bot.cogs])
		#helptext+="```"
		#await ctx.send(helptext)
		#helptext+= "WARNING : this help command is temporary."
		
		embed = discord.Embed(title=f"{self.bot.user.name} COMMAND LIST :", description="Warning : this help command is temporary and will be replaced soon.", colour=config.colour, timestamp=datetime.datetime.utcnow())
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
		
		
		embed.add_field(name="Game commands : ", value = f"""
		`{config.prefix}profile [user]` : displays the profile of a user, you by default.
		`{config.prefix}step` : make a step in the MMOBOT adventure ! Consumes energy.
		`{config.prefix}top [stat]` : displays the leaderboard for the specified stat, Exp by default.
		""", inline = False)
		embed.add_field(name="Info commands : ", value = f"""
		`{config.prefix}users` : displays a cool graph showing the number of users over time.
		`{config.prefix}info` : displays infos and stats about the bot.
		`{config.prefix}contribute` : want to contribute ? Issue the command and fill the form
		""", inline = False)
		embed.add_field(name="MISC. commands : ", value = f"""
		`{config.prefix}epic [current|next]` : displays the free games on the epic game store
		""", inline = False)
		
		await ctx.send(embed=embed)
	
	@commands.command(name="users",aliases=['stonks', 'graph', 'grow'], description="Sends a cool graph showing the number of users")
	async def users(self, ctx):
		usercount = []
		time = []

		with open('stats.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
	
			for row in csv_reader:
				usercount.append(int(row[1]))
				time.append(datetime.datetime.utcfromtimestamp(int(row[0])))
		
		oldsamples = len(usercount)
		
		try :
			step_size = len(usercount) // 500 # or any other value up to 1000, so it is in your specified limit
			usercount = usercount[::step_size]
			time = time[::step_size]
		except : 
			pass
		
		plt.figure(figsize=(18,9))
		plt.xlabel('UTC time')
		plt.xticks(rotation=20)
		plt.ylabel('users')
		plt.title(f'Data updated every 10m. Dynamic data sampling : {len(usercount)}/{oldsamples} values')
		plt.suptitle('MMOBOT users over time')
		plt.grid(b=True)
		#plt.title("i'm gay")
		plt.plot(time, usercount)
		#plt.show()
		buf = BytesIO()
		plt.savefig(buf,format="png")
		buf.seek(0)
		
		await ctx.send("<:stonks:800794117389942814>",file=discord.File(buf, "usercount.png"))
		
		log(f"{ctx.author} asked for the server infos")
		
	@commands.command(name="servers",aliases=['stonksserver', 'graphserver', 'growserver'], description="Sends a cool graph showing the number of servers")
	async def servers(self, ctx):
		servercount = []
		time = []

		with open('stats.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
	
			for row in csv_reader:
				servercount.append(int(row[2]))
				time.append(datetime.datetime.utcfromtimestamp(int(row[0])))
		
		oldsamples = len(servercount)
		
		try :
			step_size = len(servercount) // 500 # or any other value up to 1000, so it is in your specified limit
			servercount = servercount[::step_size]
			time = time[::step_size]
		except : 
			pass
			
		
		
		plt.figure(figsize=(18,9))
		plt.xlabel('UTC time')
		plt.xticks(rotation=20)
		plt.ylabel('servers')
		plt.title(f'Data updated every 10m. Dynamic data sampling : {len(servercount)}/{oldsamples} values')
		plt.suptitle('MMOBOT servers over time')
		plt.grid(b=True)
		#plt.title("i'm gay")
		plt.plot(time, servercount)
		#plt.show()
		buf = BytesIO()
		plt.savefig(buf,format="png")
		buf.seek(0)
		
		await ctx.send("<:stonks:800794117389942814>",file=discord.File(buf, "servercount.png"))
		
		log(f"{ctx.author} asked for the server infos")
	
	@commands.command(name="contribute", aliases = ['contribution', "newevent", "form", "googleform"], description = "Shows the google form in which you can contribute to the bot.")
	async def contribute(self, ctx):
		await ctx.send(f"You can contribute to the bot very easily ! If you want to add a new random event, monsters, items, commands or gameplay mechanics to MMOBOT, just follow this link and fill the form : https://forms.gle/bKdt8XUdEqmF6Bru5")	



def setup(bot):
	bot.add_cog(InfoCog(bot))
