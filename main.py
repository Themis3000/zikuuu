import os
import discord
from discord.ext import commands
from discord.ext.commands import HelpFormatter
from utils import permissions

# todo:Themi figure out a better help format method, send help to users dm.


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
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="+help"))

client.run(os.environ['TOKEN'])

# todo:Themi add more utils, especially for checking user perms
# todo:Themi add a music bot with reaction based input, especially for song skip votes
# todo:Themi add a currency and betting system, mabye even tie it into a huru like battle system
# todo:Themi add a command for repo manager only that allows him to change json config files from a command
# todo:Themi allow repo manager to reload cogs
# todo:Themi make a chat log system better then audit log
