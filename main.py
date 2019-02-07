import os
import discord
from discord.ext import commands
from discord.ext.commands import HelpFormatter
from utils import permissions


class HelpFormat(HelpFormatter):
    async def format_help_for(self, context, command_or_bot):
        if permissions.can_react(context):
            await context.message.add_reaction(chr(0x2709))
            return await super().format_help_for(context, command_or_bot)


client = commands.Bot(command_prefix='+', formatter=HelpFormat(), status=discord.Status.idle, activity=discord.Game(name="Booting..."))


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f'cogs.{name}')


@client.event
async def on_ready():
    print("Ready to rumble")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="!help"))

client.run(os.environ['TOKEN'])
