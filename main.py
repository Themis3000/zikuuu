import os
import discord
from discord.ext import commands
from discord.ext.commands import HelpFormatter
from utils import permissions
from vars import TOKEN


class HelpFormat(HelpFormatter):
    async def format_help_for(self, context, command_or_bot):
        if permissions.can_react(context):
            await context.message.add_reaction(chr(0x2709))
            return await super().format_help_for(context, command_or_bot)


client = commands.Bot(command_prefix='+', formatter=HelpFormat())


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension('cogs.' + name)

client.run(TOKEN)
