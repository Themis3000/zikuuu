from discord.ext import commands


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinz(self, ctx):
        """checks the amount of cool coinz you have"""
        pass


def setup(bot):
    bot.add_cog(Currency(bot))
