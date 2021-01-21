#this cog manages the mmo step command.

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
import formulas
import sys
from cogs import databasecommands


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
	
		if await databasecommands.discord_create_account(ctx.author, ctx):
	
	
			playerEnergy = database.get_userdata(ctx.author.id, "Energy")[0]
			playerXp = database.get_userdata(ctx.author.id, "Exp")[0]
			
			if playerEnergy > 0 :
			
				database.increase_userdata(ctx.author.id, "Energy", -1)
				
				step = random.choice(stepList)
				print(f"{ctx.author} triggered event {step[0]}.")
				expReward = random.randint(1,20)
				rewards = [('Gold', formulas.automaticGold(playerXp)), ('Exp', expReward)]
				if step[2] != "None" : 
					rewards.append((step[2], formulas.automaticLoot(playerXp, step[2])))
				embed = discord.Embed(title=f"You did one more step on your adventure !", description = "", colour = config.colour, timestamp=datetime.datetime.utcnow())
				embed.set_thumbnail(url=self.bot.user.avatar_url)
				embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
				
				embed.add_field(name="Event label", value = step[1], inline = False)
				try :
					strRewards = "\n".join([f"{emojis[r[0]]} {r[0]} : `{r[1]}`" for r in rewards])
					
				except :
					log("IMPORTANT : STEP ERROR HAS OCCURED : BAD FORMATTING.")
					log(str(rewards))
					
				for reward in rewards : 
					database.increase_userdata(ctx.author.id, reward[0], reward[1])

				embed.add_field(name="Rewards", value = strRewards, inline = False)
				await ctx.send(embed=embed)
				
				for reward in rewards : 
					if reward[0] == 'Exp':
						await check_for_level(ctx.author, ctx, reward[1])
			
			else : 
				await ctx.send(f"You try to muster all your willpower to move forward, but your body is telling you that it no longer has the strength to continue. You need some rest right now, but you will be able to explore again as soon as your energy is restored.")

	@step.error
	async def step_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else : 
			log(error)

async def check_for_level(member, ctx, amount):
	"""This should be checked AFTER adding the <amount> amount of xp to the player"""
	currentXP = database.get_userdata(member.id, 'Exp')[0]
	if formulas.levelFromXp(currentXP) > formulas.levelFromXp(currentXP-amount):
		levelAmount = formulas.levelFromXp(currentXP) - formulas.levelFromXp(currentXP-amount)
	
		await ctx.send(f"<:arrow:801026149785796638> :star: You just gained {'a' if levelAmount < 2 else levelAmount} level{'s' if levelAmount > 1 else ''} ! Congratulations ! In a soon update, you will earn competence points that will allow you to upgrade your Attack, Defense and Stamina !")

def setup(bot):
	bot.add_cog(StepCog(bot))
