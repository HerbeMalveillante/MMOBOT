# this is completely useless for now.

import discord
from discord.ext import commands
import asyncio
from log import log

class ProfileCommandsCog(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	
	@commands.command(name="cogworks", aliases = ["cw"], description = "Does the cog works ?")
	async def cogworks(self, ctx):
		await ctx.send("the cog works !")
		log(f"the cog works ! Summoned by {ctx.author}.")

def setup(bot):
	bot.add_cog(ProfileCommandsCog(bot))
