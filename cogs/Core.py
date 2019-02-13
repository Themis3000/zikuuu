from discord.ext import commands
from utils.options import Options

# todo:Themi Add more "core commands" such as a command to edit entrys in json config file

options = Options()


class Core:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx, whoa):
        """Pong!"""
        await ctx.send("Pong!")

    # @commands.command(pass_context=True)
    # async def change_config(self, ctx, option='none', new_value='none'):
    #     if option != 'none':
    #         print("option pass")
    #         if new_value != 'none':
    #             print("value pass")
    #             if option in options.check_options():
    #                 print("option legit")
    #                 if new_value in options.check_options(option) or "ANY" in options.check_options(option):
    #                     print("all pass")
    #                     options.set_current(option, new_value)
    #                     await ctx.send(f"successfully set: {option} to: {new_value}")
    #                 else:
    #                     print("4")
    #                     await ctx.send(f"I don't see that option, available options: {options.check_options(option)}")
    #             else:
    #                 print("3")
    #                 await ctx.send(f"I don't see that option, available options: {options.check_options(option)}")
    #         else:
    #             print("2")
    #             await ctx.send(f"available options: {options.check_options(option)}")
    #     else:
    #         print("1")
    #         await ctx.send(f"available options: {options.check_options()}")


def setup(bot):
    bot.add_cog(Core(bot))
