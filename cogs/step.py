import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
from log import log
import database
from configcreator import Config, EmojiList
import datetime
import random
import csv
import os


config = Config()
emojis = EmojiList().emojis



stepList = []
with open("csv/step.csv", mode = 'r', encoding='utf-8') as csv_file : 
	csv_reader = csv.reader(csv_file, delimiter = ';')
	stepList = list(csv_reader)
	log("step.csv file loaded")



class StepCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		

	@commands.cooldown(1, 5, BucketType.member) 
	@commands.command(name="step", aliases = ["s","pas", "footstep", "play"], description = "The main command of the game : use one energy point to explore the wide world of MMOBOT !")
	async def step(self,ctx):
		step = random.choice(stepList)

		rewards = [('Gold', random.randint(1,20)), ('Exp', random.randint(1,20))]
		
		embed = discord.Embed(title=f"You did one more step on your adventure !", description = "", colour = config.colour, timestamp=datetime.datetime.utcnow())
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
		
		embed.add_field(name="Event label", value = step[1], inline = False)

		strRewards = "\n".join([f"{emojis[r[0]]} {r[0]} : `{r[1]}`" for r in rewards])

		embed.add_field(name="Rewards", value = strRewards, inline = False)
		await ctx.send(embed=embed)

	@step.error
	async def step_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)



def setup(bot):
	bot.add_cog(StepCog(bot))
