from discord.ext import commands
from utils.mongo import get_user, get_coinz, change_coinz, set_coinz


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinz(self, ctx):
        """checks the amount of cool coinz you have"""
        print(ctx.user.id)
        await ctx.send(f"You have {get_coinz(ctx.user.id)} coinz")


def setup(bot):
    bot.add_cog(Currency(bot))
