from discord.ext import commands
from utils.mongo import get_user, get_coinz, change_coinz, set_coinz, faucet
import random
from utils.makeReadable import array_to_space_list, seconds_to_readable

emojis = [":bell:", ":lemon:", ":watermelon:", ":chocolate_bar:", ":cherries:", ":eggplant:", ":tangerine:", ":poop:"]
win_amounts = {":bell:": 8, ":lemon:": 4, ":watermelon:": 6, ":chocolate_bar:": 18, ":eggplant:": 10, ":tangerine:": 6}


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinz(self, ctx):
        """checks the amount of cool coinz you have"""
        await ctx.send(f"You have {get_coinz(ctx.author.id)} coinz")

    @commands.command()
    async def getcoinz(self, ctx):
        """Claim some of that mulah"""
        coinz = faucet(ctx.author.id, 30, 25200)
        if coinz[0]:
            await ctx.send(f"You have claimed 30 coinz, you now have {coinz[1]} coinz")
        else:
            await ctx.send(f"Hold on there partner, you still got some wait'n. {seconds_to_readable(coinz[1])} to go")

    @commands.command()
    async def slots(self, ctx, amount: int):
        """Lose your life savings in a game of slots!"""
        coinz = get_coinz(ctx.author.id)
        reel = []
        if amount <= coinz:
            if amount > 0:
                for i in range(0, 3):
                    reel.append(random.choice(emojis))
                if ":poop:" in reel:
                    change_coinz(ctx.author.id, -1 * amount)
                    message = "poopy spin... no win :("
                elif reel.count(":cherries:") > 0:
                    win_amount = reel.count(":cherries:") * 4
                    change_coinz(ctx.author.id, win_amount - amount)
                    if win_amount > amount:
                        message = f"Got {reel.count(':cherries:')} :cherries: and won {win_amount} coinz!"
                    else:
                        message = f"Got {reel.count(':cherries:')} :cherries: and won {win_amount} coinz, but spent {amount} on the spin"
                elif reel[0] == reel[1] and reel[1] == reel[2]:
                    win_amount = win_amounts[reel[0]] * amount
                    change_coinz(ctx.author.id, win_amount - amount)
                    message = f"Won {win_amount + amount} coinz!! Woo!"
                else:
                    change_coinz(ctx.author.id, -1 * amount)
                    message = f"no win :( lost {amount}"
                await ctx.send(array_to_space_list(reel) + "\n" + message)
            else:
                await ctx.send("You must bet more then 0")
        else:
            await ctx.send(f"You need more coinz, you currently have {coinz} coinz")

    @commands.command()
    async def slotspayouts(self, ctx):
        message = "Payout amounts:\n"
        for emoji, amount in win_amounts.items():
            message = message + "\n" + emoji + ": " + str(amount) + "x spin cost"
        message = message + "\n:cherries:: 3 credits"
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Currency(bot))
