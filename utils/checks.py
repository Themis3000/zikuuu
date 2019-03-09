from discord.ext import commands
from utils.options import check_current


def is_owner():
    def predicate(ctx):
        return str(ctx.author) in check_current("bot_owners")
    return commands.check(predicate)


def in_channel(member, channel):
    if not type(member.voice) == 'NoneType':
        return False
    else:
        return member.voice.channel.id == channel.id
