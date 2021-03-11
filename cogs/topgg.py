import dbl
import discord
from discord.ext import commands
from configcreator import Config

c = Config()


class TopGG(commands.Cog):
	"""Interaction with top.gg API"""
	
	def __init__(self, bot):
		self.bot = bot
		self.token = c.dbltoken
		self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)
		
	async def on_guild_post():
		print("Server count uploaded to top.gg")



def setup(bot):
	if c.prefix == "mmo " : # temporaire mais on upload que si le bot est bien le main
		bot.add_cog(TopGG(bot))
