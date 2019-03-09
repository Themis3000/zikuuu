from discord.ext import commands
# import random
# from utils.persistent_array import PersistentArray
import requests

# dadjokes = PersistentArray("jokes", "dadabase.txt")


class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, ctx):
        """Get a dad joke from the dada-base (aka icanhazdadjoke.com)"""
        await ctx.send(f"{requests.get(url='https://icanhazdadjoke.com/', headers={'User-Agent': 'zikuuu discord bot', 'Accept': 'text/plain'}).text}")
        # await ctx.send(random.choice(dadjokes.array))


def setup(bot):
    bot.add_cog(Jokes(bot))
