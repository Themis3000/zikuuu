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
        client.load_extension(f"cogs.{name}")


@client.event
async def on_ready():
    print("Ready to rumble")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="+help"))

# todo:Themi Move all of this to a new file
# todo:Themi fix this absolute mess of code


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(f"missing argument at {ctx.command}")
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        print(f"bad argument at {ctx.command}")
        await send_cmd_help(ctx)
    elif isinstance(error, commands.CheckFailure):
        print(f"check fail at {ctx.command}")


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = await client.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        await ctx.send("Missing an argument, use: `" + pages[0].split("\n")[1] + "`")
    else:
        pages = await client.formatter.format_help_for(ctx, ctx.command)
        await ctx.send("Incorrect argument type, use: `" + pages[0].split("\n")[1] + "`")


client.run(os.environ["TOKEN"])

# non urgent to do starts here

# todo:Themi allow repo manager to reload cogs
# todo:Themi make a chat log system better then audit log
