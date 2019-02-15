from discord.ext import commands
from utils.options import Options

options = Options()


def is_owner():
    def predicate(ctx):
        return str(ctx.author) in options.check_current("bot_owners")
    return commands.check(predicate)
