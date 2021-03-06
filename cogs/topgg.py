import dbl
from discord.ext import commands
from configcreator import Config
import requests
import json

c = Config()


class TopGG(commands.Cog):
    """Interaction with top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = c.dbltoken
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def on_guild_post():
        print("Server count uploaded to top.gg")

    @commands.command(name="vote", aliases=["topgg", "top.gg", "votetop"], description="Check if you voted on top.gg and sends you a reward if you did.")
    async def vote(self, ctx):

        headers = {
            "Authorization": c.dbltoken
        }
        params = {
            "userId": ctx.author.id
        }
        resp = json.loads(requests.get(
            "https://top.gg/api//bots/793928798298177537/check", headers=headers, params=params).text)

        await ctx.send(f"You can vote for the bot on top.gg by following this link : https://top.gg/bot/793928798298177537/vote . Thanks a lot for your support !")
        await ctx.send("You already voted for the bot, thanks !" if resp["voted"] == 1 else "You did not vote for the bot :(")


def setup(bot):
    if c.prefix == "mmo ":  # temporaire mais on upload que si le bot est bien le main
        bot.add_cog(TopGG(bot))
