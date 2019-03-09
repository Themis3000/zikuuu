from discord.ext import commands
from utils.options import check_current, check_options, set_current
from utils.makeReadable import array_to_readable
from utils.checks import is_owner


class Core:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f"Pong! I am {str(self.bot.latency*1000)[:4]}ms latent to discord servers")

    @commands.command()
    @is_owner()
    async def change_config(self, ctx, option='none'):
        """Allows the bot owner to change the bots config settings"""
        split = ctx.message.content.split(" ")
        string = ""
        for i in range(len(split) - 2):
            string = string + f" {split[i+2]}"
        new_value = string[1:]
        if option != 'none':
            if new_value != 'none':
                if option in check_options():
                    if new_value in check_options(option) or "ANY" in check_options(option):
                        set_current(option, new_value)
                        await ctx.send(f"successfully set `{option}` to `{new_value}`")
                    else:
                        await ctx.send(f"available options: `{array_to_readable(check_options(option))}`")
                else:
                    await ctx.send(f"I don't see that option, available options: `{array_to_readable(check_options(option))}`")
            else:
                await ctx.send(f"available options: `{array_to_readable(check_options(option))}`")
        else:
            await ctx.send(f"available options: `{array_to_readable(check_options())}`")


def setup(bot):
    bot.add_cog(Core(bot))
