from discord.ext import commands
from utils.options import check_current


def is_owner():
    def predicate(ctx):
        return str(ctx.author) in check_current("bot_owners")
    return commands.check(predicate)
