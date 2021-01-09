import discord
from discord.ext import commands, tasks
import asyncio
from log import log
import database
from configcreator import Config
import datetime
import time

config = Config()

class DatabaseCog(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	@commands.command(name="displaydatabase", aliases = ["dd"], description = "Displays the database content")
	async def displaydatabase(self, ctx):
		for i in database._get_whole_database():
			await ctx.send(i)
	
	@commands.command(name="getuserdata", aliases = ["gud", "ud", "userdata", "profil", "profile"], description = "Displays the profile of the given user")
	async def getuserdata(self, ctx,member: discord.Member=None):
		if not member : 
			member = ctx.author
		if await discord_create_account(member,ctx) == True :
			stats = database.get_profile(member.id)
			
			embed = discord.Embed(title=f"PROFILE OF {member}", description="", colour=config.colour, timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=self.bot.user.name + ' - requested by ' + str(ctx.author), icon_url=ctx.author.avatar_url)
			statstring = f"""
			:star: Exp : `{stats[1]}`
			<:coins:789965630434181120> Gold : `{stats[2]}`
			:zap: Energy : `{stats[3]}`/`{stats[10]*10}`
			<:diamond:796663370002071582> Diamonds : `{stats[4]}`
			"""
			embed.add_field(name="Stats", value = statstring, inline = True)
			equipmentstring = f"""
			:dagger: Weapon : `{stats[5]}`
			<:armor:796664730827751424> Armor : `{stats[6]}`
			<:backpack:796665117235478558> Backpack : `{stats[7]}`
			"""
			embed.add_field(name="Equipment", value = equipmentstring, inline = True)
			skillsstring = f"""
			:muscle: Attack : `{stats[8]}`
			:shield: Defense : `{stats[9]}`
			:runner: Stamina : `{stats[10]}`
			"""
			embed.add_field(name="Skills", value = skillsstring, inline = True)
			inventorystring = f"""
			:wood: Wood : `{stats[11]}`
			:scroll: Fabric : `{stats[12]}`
			<:iron:796670376293826590> Iron : `{stats[13]}`
			:rock: Rock : `{stats[14]}`
			:crystal_ball: Orb : `{stats[15]}`
			<:emerald:796671885525123122> Emerald : `{stats[16]}`
			<:oil_bottle:796675410397757460> Oil : `{stats[17]}`
			<:obsidian:796676716802080808> Obsidian : `{stats[18]}`
			:seedling: Seeds : `{stats[19]}`
			<:antimatter:796678615202529300> Antimatter : `{stats[20]}`
			"""
			embed.add_field(name="Inventory", value = inventorystring, inline = False)
			await ctx.send(embed=embed)
			log(f"{ctx.author} displayed the profile of {member}")
	
	@getuserdata.error
	async def getuserdata_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Sorry, we could not find this member")
			log(f"{ctx.author} tried to display the profile of a member but it could not be found.")
	
	@commands.command(name="setstat", aliases = ["ss"], description = "[ADMIN]")
	async def setstat(self, ctx, member : discord.Member=None, stat = None, value = None):
		if ctx.author.id in config.admins:
			try:
				database.modify_userdata(member.id, stat, int(value))
				await ctx.send(f"Changed stat {stat} for user {member} to value {value}")
			except : 
				await ctx.send(f"Oops : Something went wrong. Please check your syntax : {config.prefix}setstat [member] [stat] [value]")
		else : 
			await ctx.send(f"Sorry, this command is only for admins.")

	@setstat.error
	async def setstat_error(self, ctx, error):
		if isinstance(error, commands.MemberNotFound):
			await ctx.send(f"User not found ! Check command usage : {config.prefix}setstat [user] [stat] [value]")

	@commands.command(name="addstat", aliases=['as', 'add'], description = "[ADMIN]")
	async def addstat(self, ctx, member: discord.Member=None, stat = None, value = None):
		if ctx.author.id in config.admins : 
			database.increase_userdata(member.id, stat, int(value))
			try : 
				
				await ctx.send(f"Increased stat {stat} for user {member} by {value}")
			except : 
				await ctx.send(f"Oops : Something went wrong. Please check your syntax : {config.prefix}addstat [member] [stat] [value]")
		else : 
			await ctx.send(f"Sorry, this command is only for admins.")

	@addstat.error
	async def addstat_error(self, ctx, error):
		if isinstance(error, commands.MemberNotFound):
			await ctx.send(f"User not found ! Check command usage : {config.prefix}addstat [user] [stat] [value]")



	@tasks.loop(seconds=600.0)
	async def energy(self):
		timestart = datetime.datetime.now().timestamp()
		database.increment_energy()
		log(f"[LOOP] Energy recovered in {datetime.datetime.now().timestamp() - timestart}s")
		


async def discord_create_account(member,ctx):
	if not database.does_account_exists(member.id):
		if member != ctx.author :
			if ctx.author.id in config.admins :
				database.create_account(member.id)
				log(f"{ctx.author} created an account for user {member}")
			else : 
				await ctx.send("Sorry ! You can't create a profile for another user.")
				log(f"{ctx.author} tried to create an account for {member} but is unauthorised.")
				return False
		else :
			database.create_account(member.id)
			await member.send("Hello ! We received a mail to prevent us that you created an account on MMOBOT : congratulations ! Join the official server here : [the bot does not have an official server for now]")
			log(f"{ctx.author} just created an account !")



	return True


def setup(bot):
	bot.add_cog(DatabaseCog(bot))