from discord.ext import commands
import requests


class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, ctx):
        """Get a dad joke from the dada-base (aka icanhazdadjoke.com)"""
        joke = requests.get(url='https://icanhazdadjoke.com/',
                     headers={'User-Agent': 'zikuuu discord bot (https://github.com/Themis3000/zikuuu)', 'Accept': 'text/plain'}).text.replace("â", "'")
        await ctx.send(joke)


def setup(bot):
    bot.add_cog(Jokes(bot))
