# this cog manages the mmo step command.

import discord
from discord.ext import commands
from log import log
import database
from configcreator import Config, EmojiList
import datetime
import random
import csv
import formulas
from cogs import databasecommands


config = Config()
emojis = EmojiList().emojis


stepList = []
with open("csv/step.csv", mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    stepList = list(csv_reader)
    log("step.csv file loaded")


class StepCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.cooldown(1, 3, BucketType.member)

    @commands.command(name="step", aliases=["s", "pas", "footstep", "play"], description="The main command of the game : use one energy point to explore the wide world of MMOBOT !")
    async def step(self, ctx):

        if await databasecommands.discord_create_account(ctx.author, ctx):

            playerEnergy = database.get_userdata(ctx.author.id, "Energy")[0]
            playerXp = database.get_userdata(ctx.author.id, "Exp")[0]

            if playerEnergy > 0:

                database.increase_userdata(ctx.author.id, "Energy", -1, False)

                step = random.choice(stepList)
                print(f"{ctx.author} triggered event {step[0]}.")
                expReward = random.randint(15, 25)
                rewards = [('Gold', formulas.automaticGold(
                    playerXp)), ('Exp', expReward)]
                if step[2] != "None":
                    rewards.append(
                        (step[2], formulas.automaticLoot(playerXp, step[2])))
                embed = discord.Embed(title=f"You did one more step on your adventure !",
                                      description="", colour=config.colour, timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=self.bot.user.name + ' - requested by ' +
                                 str(ctx.author), icon_url=ctx.author.avatar_url)

                embed.add_field(name="Event label",
                                value=step[1], inline=False)
                try:
                    strRewards = "\n".join(
                        [f"{emojis[r[0]]} {r[0]} : `{r[1]}`" for r in rewards])

                except:
                    log("IMPORTANT : STEP ERROR HAS OCCURED : BAD FORMATTING.")
                    log(str(rewards))

                for reward in rewards:
                    database.increase_userdata(
                        ctx.author.id, reward[0], reward[1], False)

                embed.add_field(name="Rewards", value=strRewards, inline=False)
                await ctx.send(embed=embed)

                for reward in rewards:
                    if reward[0] == 'Exp':
                        await check_for_level(ctx.author, ctx, reward[1])

            else:
                await ctx.send(f"You try to muster all your willpower to move forward, but your body is telling you that it no longer has the strength to continue. You need some rest right now, but you will be able to explore again as soon as your energy is restored.")

    @step.error
    async def step_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            log(error)

    @commands.command(name="autostep", aliases=["autopas", "mercenaire"], description="An automatic version of the step command, but you don't get all the rewards !")
    async def autostep(self, ctx, energy: int = None):
        if await databasecommands.discord_create_account(ctx.author, ctx):
            if energy is None:
                energy = int(database.get_userdata(ctx.author.id, "Energy")[0])

            if energy <= 0:
                await ctx.send("I'm sorry, you can't take a step with 0 energy or less.")
                return
            elif energy > int(database.get_userdata(ctx.author.id, "Energy")[0]):
                await ctx.send(f"I'm sorry, you don't have enough energy to perform {energy} automatic steps.")
                return

            playerXp = database.get_userdata(ctx.author.id, "Exp")[0]

            expReward = random.randint(15, 25) * energy
            goldReward = formulas.automaticGold(playerXp) * energy

            rewards = {
                "Gold": goldReward,
                "Exp": expReward
            }

            for i in range(energy):
                step = random.choice(stepList)

                if step[2] != "None":
                    if step[2] not in list(rewards.keys()):
                        rewards[step[2]] = formulas.automaticLoot(
                            playerXp, step[2])
                    else:
                        rewards[step[2]
                                ] += formulas.automaticLoot(playerXp, step[2])

            embed = discord.Embed(title=f"The mercenary has arrived !",
                                  description=f"Use command `{config.prefix}autostep <energy>` to autostep for a certain amount of energy.", colour=config.colour, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=self.bot.user.name + ' - requested by ' +
                             str(ctx.author), icon_url=ctx.author.avatar_url)

            embed.add_field(name="Event label",
                            value=f"You've hired a mercenary to take a **{energy}**-step journey for you. In exchange, it requires 30% of the resources recovered. You reluctantly agree.", inline=False)
            try:
                strRewards = "\n".join(
                    [f"{emojis[r]} {r} : `{int(round(rewards[r] * 0.7))}`" for r in list(rewards.keys())])
                embed.add_field(name="Rewards", value=strRewards, inline=False)
            except:
                log("IMPORTANT : STEP ERROR HAS OCCURED : BAD FORMATTING.")
                log(str(rewards))
                await ctx.send("A bad syntax error has occured in one of the events. You did not lost any energy. Please report this error to a developer.")
                return

            database.increase_userdata(ctx.author.id, "Energy", -energy, False)

            for r in list(rewards.keys()):
                database.increase_userdata(
                    ctx.author.id, r, int(round(rewards[r] * 0.7)), False)

            await ctx.send(embed=embed)
            await check_for_level(ctx.author, ctx, rewards["Exp"])
            log(f"{ctx.author} autostepped for {energy} energy.")

    @autostep.error
    async def autostep_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"Usage : `{config.prefix}autostep <energy amount>`")
        else:
            log(error)


async def check_for_level(member, ctx, amount):
    """This should be checked AFTER adding the <amount> amount of xp to the player"""
    currentXP = database.get_userdata(member.id, 'Exp')[0]
    if formulas.levelFromXp(currentXP) > formulas.levelFromXp(currentXP - amount):
        levelAmount = formulas.levelFromXp(
            currentXP) - formulas.levelFromXp(currentXP - amount)

        await ctx.send(f"<:arrow:801026149785796638> :star: You just gained {'a' if levelAmount < 2 else levelAmount} level{'s' if levelAmount > 1 else ''} ! Congratulations !\nYou earned {'a' if levelAmount < 2 else levelAmount} Competence Point{'s' if levelAmount > 1 else ''} :medal: that you can use to upgrade your Attack, Defense and Stamina with the `{config.prefix}upgrade` command !")
        database.increase_userdata(ctx.author.id, "Points", levelAmount, False)
        print(f"{ctx.author} gained a level.")


def setup(bot):
    bot.add_cog(StepCog(bot))
