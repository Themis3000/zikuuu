from discord.ext import commands
from utils.mongo import get_user, get_coinz, change_coinz, set_coinz, faucet


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinz(self, ctx):
        """checks the amount of cool coinz you have"""
        print(ctx.author.id)
        await ctx.send(f"You have {get_coinz(ctx.author.id)} coinz")

    @commands.command()
    async def get_coinz(self, ctx):
        """Claim some of that mulah"""
        coinz = faucet(ctx.author.id, 10, 10)
        if coinz:
            await ctx.send(f"You have claimed 10 coinz, you now have {coinz} coinz")
        else:
            await ctx.send("Hold on there partner, you still got some wait'n")


def setup(bot):
    bot.add_cog(Currency(bot))
