from utils.options import Options
import os
import discord
from discord.ext import commands

# todo:Themi figure out a better help format method, send help to users dm.

options = Options()
client = commands.Bot(command_prefix='+', status=discord.Status.idle, activity=discord.Game(name="Booting..."))


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f'cogs.{name}')


@client.event
async def on_ready():
    print("Ready to rumble")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="+help"))


@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = client.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await ctx.send_message(page)
    else:
        pages = client.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await ctx.send_message(page)


client.run(os.environ["TOKEN"])

# todo:Themi add a !allow command to allow one time access to a voice channel
# todo:Themi add more utils, especially for checking user perms
# todo:Themi add a music bot with reaction based input, especially for song skip votes
# todo:Themi add a currency and betting system, mabye even tie it into a huru like battle system
# todo:Themi add a command for repo manager only that allows him to change json config files from a command
# todo:Themi allow repo manager to reload cogs
# todo:Themi make a chat log system better then audit log
