# adds commands that interact with the database (see data, add data, etc)

import discord
from discord.ext import commands, tasks
import asyncio
from log import log
import database
from configcreator import Config, EmojiList
import datetime
import sys
import traceback
import formulas
from cogs import step

config = Config()
emojiList = EmojiList()


class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="displaydatabase", aliases=["dd"], description="Displays the database content")
    async def displaydatabase(self, ctx):
        for i in database._get_whole_database():
            await ctx.send(i)

    @commands.command(name="getuserdata", aliases=["gud", "ud", "userdata", "profil", "profile"], description="Displays the profile of the given user")
    async def getuserdata(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        if await discord_create_account(member, ctx) == True:
            stats = database.get_profile(member.id)

            embed = discord.Embed(
                title=f"PROFILE OF {member}", description="", colour=config.colour, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=self.bot.user.name + ' - requested by ' +
                             str(ctx.author), icon_url=ctx.author.avatar_url)
            level = formulas.levelFromXp(stats[1])
            statstring = f"""
            :star: Level : `{level} ({stats[1]}/{formulas.xpFromLevel(level+1)})`
            <:coins:789965630434181120> Gold : `{stats[2]}`
            :zap: Energy : `{stats[3]}`/`{stats[10]*10}`
            <:diamond:796663370002071582> Diamonds : `{stats[4]}`
            :medal: Competence Points : `{stats[21]}`
            """
            embed.add_field(name="Stats", value=statstring, inline=True)
            equipmentstring = f"""
            :dagger: Weapon : `{stats[5]}`
            <:armor:796664730827751424> Armor : `{stats[6]}`
            <:backpack:796665117235478558> Backpack : `{stats[7]}`
            """
            embed.add_field(name="Equipment",
                            value=equipmentstring, inline=True)
            skillsstring = f"""
            :muscle: Attack : `{stats[8]}`
            :shield: Defense : `{stats[9]}`
            :runner: Stamina : `{stats[10]}`
            """
            embed.add_field(name="Skills", value=skillsstring, inline=True)
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
            embed.add_field(name="Inventory",
                            value=inventorystring, inline=False)
            await ctx.send(embed=embed)
            log(f"{ctx.author} displayed the profile of {member}")

    @getuserdata.error
    async def getuserdata_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Sorry, we could not find this member")
            log(f"{ctx.author} tried to display the profile of a member but it could not be found.")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="setstat", aliases=["ss"], description="[ADMIN]")
    async def setstat(self, ctx, member: discord.Member=None, stat=None, value=None):
        if ctx.author.id in config.admins:
            try:
                database.modify_userdata(member.id, stat, int(value), False)
                # await ctx.send(f"Changed stat {stat} for user {member} to value {value}")
                if stat == "Exp":
                    await step.check_for_level(member, ctx, int(value))

            except:
                await ctx.send(f"Oops : Something went wrong. Please check your syntax : {config.prefix}setstat [member] [stat] [value]")

        else:
            await ctx.send(f"Sorry, this command is only for admins.")

    @setstat.error
    async def setstat_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"User not found ! Check command usage : {config.prefix}setstat [user] [stat] [value]")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="addstat", aliases=['as', 'add'], description="[ADMIN]")
    async def addstat(self, ctx, member: discord.Member=None, stat=None, value=None):
        if ctx.author.id in config.admins:
            try:
                database.increase_userdata(member.id, stat, int(value), False)
                await ctx.send(f"Increased stat {stat} for user {member} by {value}")
                if stat == "Exp":
                    await step.check_for_level(member, ctx, int(value), False)

            except:
                await ctx.send(f"Oops : Something went wrong. Please check your syntax : {config.prefix}addstat [member] [stat] [value]")

        else:
            await ctx.send(f"Sorry, this command is only for admins.")

    @addstat.error
    async def addstat_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"User not found ! Check command usage : {config.prefix}addstat [user] [stat] [value]")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="reset", aliases=['delete', 'restart'], description="[ADMIN] resets another user's stats.")
    async def reset(self, ctx, member: discord.Member=None):
        if ctx.author.id in config.admins:

            try:
                database.delete_userdata(member.id)
                await ctx.send(f"Resetted account for user {member}")
            except AttributeError:
                await ctx.send(f"Oops : Something went wrong. Please check your syntax : {config.prefix}reset [member]")
        else:
            await ctx.send(f"Sorry, this command is only for admins.")

    @reset.error
    async def reset_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"User not found ! Check command usage : {config.prefix}reset [member]")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name="top", aliases=['leaderboard'], description="Gives the leaderboard of the bot based on the specified stat")
    async def top(self, ctx, stat="Exp"):
        try:
            top = database.get_top(stat, 10)
        except:
            await ctx.send(f"Stat `{stat}` not found ! Please check your spelling.")
            return

        embed = discord.Embed(
            title=f"LEADERBOARD FOR STAT {stat}", description=f"Use `{config.prefix}top [stat]` to show the leaderboard for a precise stat.", colour=config.colour, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/799748441172738048/804047014492635196/trophy.png")
        embed.set_footer(text=self.bot.user.name + ' - requested by ' +
                         str(ctx.author), icon_url=ctx.author.avatar_url)

        playerList = []
        for i in range(len(top)):
            member = str(self.bot.get_user(top[i][0]))
            if member != 'None':
                playerList.append([str(member), top[i][1]])

        topString = '\n'.join(
            [f"**#{i+1}** - {playerList[i][0]} : `{playerList[i][1]} {stat}`" for i in range(len(playerList))])

        embed.add_field(
            name=f"top {len(top)} users in this category :", value=topString, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="upgrade", aliases=['craft'], description=f"Upgrade a stat of your choice")
    async def upgrade(self, ctx, stat=None):
        await discord_create_account(ctx.author, ctx)
        upgradables = ['ATTACK', 'DEFENSE', 'STAMINA']
        if stat == None:
            await ctx.send(f"You must specify a stat to upgrade ! Usage : `{config.prefix}upgrade [stat]`.")
            return
        elif stat.upper() not in upgradables:
            await ctx.send(f"Upgradable stat `{stat}` not found ! Please check your spelling.")
            return

        authorStats = database.get_profile(ctx.author.id)
        pointsStats = authorStats[21]
        goldStats = authorStats[2]
        orbStats = authorStats[15]
        oilStats = authorStats[17]
        seedsStats = authorStats[19]
        fabricStats = authorStats[12]

        currentLevel = database.get_userdata(ctx.author.id, stat)[0]
        embed = discord.Embed(title=f"UPGRADE SKILL {stat.upper()} {emojiList.emojis[stat.title()]} | {currentLevel} :arrow_forward: {currentLevel+1}",
                              description=f"Click on a reaction within `{config.timeout}` seconds to confirm or decline the upgrade.", colour=config.colour, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        price = formulas.coutUpgradeSkills(currentLevel + 1)
        priceStr = "\n".join(
            f"{emojiList.emojis[stat]} {stat} : `{database.get_userdata(ctx.author.id, stat)[0]}`/`{price[stat]}`" for stat in price.keys())
        embed.add_field(name="Price :", value=priceStr, inline=False)
        embed.set_footer(text=self.bot.user.name + ' - requested by ' +
                         str(ctx.author), icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("🚫")

        def check(r, u):
            checkBool = u.id == ctx.author.id and (not u.bot) and r.message.id == message.id and (
                str(r.emoji) == "✅" or str(r.emoji) == "🚫")
            return checkBool
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=config.timeout)
        except asyncio.TimeoutError:
            log(f"Delay for {ctx.author.id} to upgrade {stat} has expired.")
        else:
            if str(reaction.emoji) == "🚫":
                await ctx.send("Upgrade cancelled.")
                return
            elif str(reaction.emoji) == "✅":

                boolRich = pointsStats >= price["Points"] and goldStats >= price["Gold"] and orbStats >= price[
                    "Orb"] and oilStats >= price["Oil"] and seedsStats >= price["Seeds"] and fabricStats >= price["Fabric"]
                if boolRich:

                    database.increase_userdata(
                        ctx.author.id, "Points", -price['Points'], False)
                    database.increase_userdata(
                        ctx.author.id, "Gold", -price['Gold'], False)
                    database.increase_userdata(
                        ctx.author.id, "Orb", -price['Orb'], False)
                    database.increase_userdata(
                        ctx.author.id, "Oil", -price['Oil'], False)
                    database.increase_userdata(
                        ctx.author.id, "Seeds", -price['Seeds'], False)
                    database.increase_userdata(
                        ctx.author.id, "Fabric", -price['Fabric'], False)
                    database.increase_userdata(
                        ctx.author.id, stat.upper(), 1, False)

                    await ctx.send(f"You successfully upgraded the stat `{stat}` to level `{currentLevel+1}` !")
                else:
                    await ctx.send("I'm sorry, but you're not rich enough to upgrade this stat.")
                return

    @tasks.loop(seconds=600.0)
    async def energy(self):
        timestart = datetime.datetime.now().timestamp()
        database.increment_energy()
        log(
            f"[LOOP] Energy recovered in {datetime.datetime.now().timestamp() - timestart}s")


async def discord_create_account(member, ctx):
    if not database.does_account_exists(member.id):
        if member != ctx.author:
            if ctx.author.id in config.admins:
                database.create_account(member.id)
                log(f"{ctx.author} created an account for user {member}")
            else:
                await ctx.send("Sorry ! You can't create a profile for another user.")
                log(f"{ctx.author} tried to create an account for {member} but is unauthorised.")
                return False
        else:
            database.create_account(member.id)
            await member.send("Hello ! We received a mail to prevent us that you created an account on MMOBOT : congratulations ! Join the official server here : https://discord.gg/vRA4gdraaC")
            log(f"{ctx.author} just created an account !")

    return True


def setup(bot):
    bot.add_cog(DatabaseCog(bot))
