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
		playerEnergy = database.get_userdata(ctx.author.id, "Energy")[0]
		
		if playerEnergy > 0 :
		
			database.increase_userdata(ctx.author.id, "Energy", -1)
			
			step = random.choice(stepList)
			print(f"{ctx.author} triggered event {step[0]}.")
			
			rewards = [('Gold', random.randint(1,20)), ('Exp', random.randint(1,20))]
			if step[2] != "None" : 
				rewards.append((step[2], random.randint(1,20)))
			embed = discord.Embed(title=f"You did one more step on your adventure !", description = "", colour = config.colour, timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=self.bot.user.avatar_url)
			embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
			
			embed.add_field(name="Event label", value = step[1], inline = False)
			try :
				strRewards = "\n".join([f"{emojis[r[0]]} {r[0]} : `{r[1]}`" for r in rewards])
				
			except :
				log("IMPORTANT : STEP ERROR HAS OCCURED : BAD FORMATTING.")
				log(rewards)
				
			for reward in rewards : 
				database.increase_userdata(ctx.author.id, reward[0], reward[1])

			embed.add_field(name="Rewards", value = strRewards, inline = False)
			await ctx.send(embed=embed)
		
		else : 
			await ctx.send(f"I'm sorry {ctx.author}, but you can't explore anymore as you're out of energy. Take some rest and try again a bit later !")

	@step.error
	async def step_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else : 
			log(error)



def setup(bot):
	bot.add_cog(StepCog(bot))
