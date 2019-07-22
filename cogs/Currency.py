from discord.ext import commands
from utils.mongo import get_user, get_coinz, change_coinz, faucet, new_pet, battle_results, start_raid, end_raid, set_coinz
import random
from utils.makeReadable import array_to_space_list, seconds_to_readable
from utils.options import check_current
import asyncio
import discord
import time

sent_requests = []
pets = ["🐱", "🐭", "🐶", "🐷", "🐮", "🐔", "🦁"]
emojis = [":bell:", ":gem:", ":cherries:", ":eggplant:", ":tangerine:", ":poop:"]
win_amounts = {":bell:": 8, ":gem:": 18, ":eggplant:": 10, ":tangerine:": 6}
raids = {"1⃣": {"time": 5400, "coinz": 5, "addition_potential": 5}, "2⃣": {"time": 10800, "coinz": 15, "addition_potential": 15}, "3⃣": {"time": 21600, "coinz": 30, "addition_potential": 30}, "4⃣": {"time": 43200, "coinz": 60, "addition_potential": 60}}


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinz(self, ctx):
        """checks the amount of cool coinz you have"""
        await ctx.send(f"You have {get_coinz(ctx.author.id)} coinz")

    @commands.command()
    async def getcoinz(self, ctx):
        """Claim some of that mulah"""
        amount = 30
        coinz = faucet(ctx.author.id, amount, 25200)
        if coinz[0]:
            await ctx.send(f"You have claimed {amount} coinz, you now have {coinz[1]} coinz")
        else:
            await ctx.send(f"Hold on there partner, you still got some wait'n. {seconds_to_readable(coinz[1])} to go")

    @commands.command()
    async def slots(self, ctx, amount: int):
        """Lose your life savings in a game of slots!"""
        coinz = get_coinz(ctx.author.id)
        reel = []
        if amount <= coinz:
            if amount > 0:
                for i in range(0, 3):
                    reel.append(random.choice(emojis))
                if ":poop:" in reel:
                    set_coinz(ctx.author.id, coinz - amount)
                    message = "poopy spin... no win :("
                elif reel.count(":cherries:") > 0:
                    win_amount = reel.count(":cherries:") * 4
                    set_coinz(ctx.author.id, coinz + win_amount - amount)
                    if win_amount > amount:
                        message = f"Got {reel.count(':cherries:')} :cherries: and won {win_amount} coinz!"
                    else:
                        message = f"Got {reel.count(':cherries:')} :cherries: and won {win_amount} coinz, but spent {amount} on the spin"
                elif reel[0] == reel[1] and reel[1] == reel[2]:
                    win_amount = win_amounts[reel[0]] * amount
                    set_coinz(ctx.author.id, coinz + win_amount - amount)
                    message = f"Won {win_amount + amount} coinz!! Woo!"
                else:
                    set_coinz(ctx.author.id, coinz - amount)
                    message = f"no win :( lost {amount}"
                await ctx.send(array_to_space_list(reel) + "\n" + message)
            else:
                await ctx.send("You must bet more then 0")
        else:
            await ctx.send(f"You need more coinz, you currently have {coinz} coinz")

    @commands.command()
    async def slotspayouts(self, ctx):
        """Get tempted into playing slots"""
        message = "Payout amounts:\n"
        for emoji, amount in win_amounts.items():
            message = message + "\n" + emoji + ": " + str(amount) + "x spin cost"
        message = message + "\n:cherries:: 3 credits"
        await ctx.send(message)

    @commands.command()
    async def buypet(self, ctx):
        """Get yo self a pet for your travels"""
        cost = 20
        user = get_user(ctx.author.id)

        if user["coinz"] >= cost:
            message = await ctx.send(f"Choose your pet emoji (Buying a pet costs {cost} coinz)")
            for emoji in pets:
                await message.add_reaction(emoji)

            def check_pet(reaction, user):
                return user == ctx.author and reaction.emoji in pets

            try:
                reaction, sender = await self.bot.wait_for('reaction_add', timeout=120, check=check_pet)
            except asyncio.TimeoutError:
                await ctx.send("You took too long...")
            else:
                await ctx.send(f"You chose {reaction}! What do you want to name your pet? Use {check_current('prefix')}name (name). (Note: buying a new pet will get rid of your old pet)")

                def check_name(m):
                    return m.author == ctx.author and m.content.split(" ")[0] == f"{check_current('prefix')}name"

                try:
                    name_msg = await self.bot.wait_for("message", timeout=120, check=check_name)
                except asyncio.TimeoutError:
                    await ctx.send("You took too long...")
                else:
                    name_array = name_msg.content.split(" ")
                    name_array.pop(0)
                    name = array_to_space_list(name_array)
                    if len(name) < 20:
                        new_pet(user, name, reaction.emoji, cost)
                        await ctx.send(f"Have fun with your new buddy {name}!")
                    else:
                        await ctx.send("You cannot have your name be over 20 characters")
        else:
            await ctx.send(f"You must have at least {cost} coinz in order to do this")

    @commands.command()
    async def battle(self, ctx, defending: discord.Member, amount: int):
        """Heck someone up and take their coinz gang gang style"""
        if not ctx.author == defending:
            user = get_user(ctx.author.id)
            defending_user = get_user(defending.id)
            min = 10
            if "raid" not in user or not user["raid"]["end_time"] > time.time():
                if "raid" not in defending_user or not defending_user["raid"]["end_time"] > time.time():
                    if amount >= min:
                        if "pet" in user:
                            if "pet" in defending_user:
                                if user["coinz"] >= amount:
                                    if defending_user["coinz"] >= amount:
                                        if [ctx.author.id, defending.id] not in sent_requests:
                                            sent_requests.append([ctx.author.id, defending.id])
                                            accept_message = await ctx.send(f"{defending.mention} has been challenged by {ctx.author.mention} for {amount} coinz. Accept by clicking the :white_check_mark: (they have 120 seconds to respond)")
                                            await accept_message.add_reaction("✅")
                                            await accept_message.add_reaction("❌")

                                            def check_accept(reaction, sender):
                                                return sender == defending and reaction.emoji in ["✅", "❌"] and reaction.message.id == accept_message.id or sender == ctx.author and reaction.emoji == "❌" and reaction.message.id == accept_message.id

                                            try:
                                                reaction, sender = await self.bot.wait_for('reaction_add', timeout=120, check=check_accept)
                                            except asyncio.TimeoutError:
                                                sent_requests.remove([ctx.author.id, defending.id])
                                                await accept_message.add_reaction("⏰")
                                                await ctx.send(f"{defending.mention} took to long to respond.")
                                            else:
                                                sent_requests.remove([ctx.author.id, defending.id])
                                                if reaction.emoji == "❌":
                                                    await accept_message.add_reaction("🛑")
                                                    await ctx.send(f"Battle canceled by {sender.mention}")
                                                else:
                                                    change_coinz(ctx.author.id, -1 * amount)
                                                    change_coinz(defending.id, -1 * amount)
                                                    # game loop
                                                    game_message = await ctx.send(f"starting...")
                                                    game_playing = True
                                                    user_hp = 10
                                                    defending_hp = 10
                                                    max_hp = 10
                                                    user_turn = True
                                                    turncount = 0
                                                    while game_playing:
                                                        if user_hp > 0:
                                                            if defending_hp > 0:
                                                                block_string = " "
                                                                # logic for attacking users move
                                                                if max_hp > user_hp:
                                                                    attack_rand_int = random.randint(1, 10)
                                                                    if attack_rand_int >= 9:
                                                                        attack_move = "heal"
                                                                        attack_emote = ":sparkling_heart:"
                                                                    else:
                                                                        attack_move = "attack"
                                                                        attack_emote = ":crossed_swords:"
                                                                else:
                                                                    attack_move = "attack"
                                                                    attack_emote = ":crossed_swords:"
                                                                # logic for defending users move
                                                                defend_rand_int = random.randint(1, 10)
                                                                if defend_rand_int >= 8:
                                                                    defend_move = "block"
                                                                    defending_emote = ":octagonal_sign:"
                                                                else:
                                                                    defend_move = "nothing"
                                                                    defending_emote = ":zzz:"
                                                                # logic for damage changes
                                                                if attack_move == "heal":
                                                                    if user_turn:
                                                                        user_hp = user_hp + 1
                                                                    else:
                                                                        defending_hp = defending_hp + 1
                                                                elif attack_move == "attack" and defend_move == "block":
                                                                    block_string = "Blocked!"
                                                                else:
                                                                    if user_turn:
                                                                        defending_hp = defending_hp - 1
                                                                    else:
                                                                        user_hp = user_hp - 1
                                                                # logic for setting name of turn and swapping turns
                                                                if user_turn:
                                                                    user_emote = attack_emote
                                                                    defending_emote = defending_emote
                                                                    user_pointer = "<==="
                                                                    defending_pointer = ""
                                                                    user_turn = False
                                                                else:
                                                                    user_emote = defending_emote
                                                                    defending_emote = attack_emote
                                                                    user_pointer = ""
                                                                    defending_pointer = "<==="
                                                                    user_turn = True
                                                                turncount = turncount + 1
                                                                user_hearts = ((user_hp//2) * ":heart:") + ((user_hp % 2) * ":broken_heart:") + (((max_hp-user_hp)//2) * ":black_heart:")
                                                                defending_hearts = ((defending_hp//2) * ":heart:") + ((defending_hp % 2) * ":broken_heart:") + (((max_hp-defending_hp)//2) * ":black_heart:")
                                                                await game_message.edit(content=f"{user_emote} {user_pointer}\n{user_hearts}{user['pet']['emote']}{user['pet']['name']}({ctx.author.mention})\nturn:{turncount}       {block_string}\n{defending_hearts}{defending_user['pet']['emote']}{defending_user['pet']['name']}({defending.mention})\n{defending_emote} {defending_pointer}")
                                                                await asyncio.sleep(1)
                                                            else:
                                                                battle_results(ctx.author.id, defending.id, amount)
                                                                await ctx.send(f"{ctx.author.mention} Has won the battle for {amount} coinz!")
                                                                game_playing = False
                                                        else:
                                                            battle_results(defending.id, ctx.author.id, amount)
                                                            await ctx.send(f"{defending.mention} Has won the battle for {amount} coinz!")
                                                            game_playing = False
                                        else:
                                            await ctx.send(f"You can only have one request out to a person at a time")
                                    else:
                                        await ctx.send("The person you challenged does not have enough coinz")
                                else:
                                    await ctx.send("You do not have enough coinz")
                            else:
                                await ctx.send(f"The person who you challenged does not have a pet, use {check_current('prefix')}buypet to buy one")
                        else:
                            await ctx.send("You need a pet to play, use +pet to buy one")
                    else:
                        await ctx.send(f"You need to bet at least {min} coinz")
                else:
                    await ctx.send("The person you challenged does is currently in a raid so they cannot battle")
            else:
                await ctx.send("You are currently in a raid so you cannot battle")
        else:
            await ctx.send("You cannot battle yourself")

    @commands.command()
    async def stats(self, ctx):
        """Show off your superiority"""
        user = get_user(ctx.author.id)
        if user["pet"]:
            await ctx.send(f"Your pet {user['pet']['name']}'s stats:\nWins: {user['pet']['win']}\nLosses: {user['pet']['loss']}")
        else:
            await ctx.send("You do not have a pet!")

    @commands.group()
    async def raid(self, ctx):
        """Raid commands help"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @raid.command()
    async def status(self, ctx):
        """Check on the status of your raid"""
        user = get_user(ctx.author.id)
        if "raid" in user:
            if user["raid"]["end_time"] < time.time():
                await ctx.send(f"{ctx.author.mention} {user['pet']['emote']} {user['pet']['name']} has returned from a raid with {user['raid']['reward']} coinz!")
                end_raid(ctx.author.id)
            else:
                await ctx.send(f"{ctx.author.mention} {user['pet']['emote']} {user['pet']['name']} is currently in a raid for another {seconds_to_readable(user['raid']['end_time'] - int(time.time()))}")
        else:
            await ctx.send(f"{ctx.author.mention} {user['pet']['emote']} {user['pet']['name']} is not currently in a raid")

    @raid.command()
    async def start(self, ctx):
        """Start a raid"""
        user = get_user(ctx.author.id)
        if "pet" in user:
            if "raid" not in user or not user["raid"]["end_time"] > time.time():
                if "raid" in user and user["raid"]["end_time"] < time.time():
                    await ctx.send(f"{ctx.author.mention} {user['pet']['emote']} {user['pet']['name']} has returned from a raid with {user['raid']['reward']} coinz!")
                    end_raid(ctx.author.id)
                selection = await ctx.send("Keep in mind when you send your pet on a raid you cannot interact with them until they get back, this includes battles\n\n"
                                           "What difficulty would you like?\n"
                                           ":one:: easy - 1.5 hours, up to 10 coinz\n"
                                           ":two:: medium - 3 hours, up to 30 coinz\n"
                                           ":three:: hard - 6 hours, up to 60 coinz\n"
                                           ":four:: very hard - 12 hours, up to 120 coinz\n")
                await selection.add_reaction("1⃣")
                await selection.add_reaction("2⃣")
                await selection.add_reaction("3⃣")
                await selection.add_reaction("4⃣")

                def check_difficulty(reaction, sender):
                    return sender == ctx.author and reaction.emoji in ["1⃣", "2⃣", "3⃣", "4⃣"] and reaction.message.id == selection.id

                try:
                    difficulty, sender = await self.bot.wait_for('reaction_add', timeout=120, check=check_difficulty)
                except asyncio.TimeoutError:
                    await selection.add_reaction("⏰")
                else:
                    await selection.clear_reactions()
                    await selection.edit(content="Would you like to allow others to join the raid?")
                    await selection.add_reaction("✅")
                    await selection.add_reaction("❌")

                    def check_open(reaction, sender):
                        return sender == ctx.author and reaction.emoji in ["✅", "❌"] and reaction.message.id == selection.id

                    try:
                        reaction, sender = await self.bot.wait_for('reaction_add', timeout=120, check=check_open)
                    except asyncio.TimeoutError:
                        await selection.add_reaction("⏰")
                    else:
                        await selection.delete()

                        if reaction.emoji == "✅":
                            party = await ctx.send(f"If you would like to send off your pet join {ctx.author.mention}'s raid that will take {seconds_to_readable(raids[difficulty.emoji]['time'])} hours and yield up to {raids[difficulty.emoji]['coinz'] + raids[difficulty.emoji]['addition_potential']} coinz, hit :white_check_mark:. for every person that joins a 30% bonus is added. Press :play_pause: to start the raid or  will automatically start if no one joins for 4 minutes\n\n"
                                                   "Keep in mind when you send your pet on a raid you cannot interact with your pet until they get back, this includes battles.")
                            await party.add_reaction("✅")
                            await party.add_reaction("⏯")
                            await party.add_reaction("❌")

                            def check_group(reaction, sender):
                                return reaction.emoji in ["⏯", "❌", "✅"] and reaction.message.id == party.id

                            group = [ctx.author.id]

                            while True:
                                try:
                                    reaction, sender = await self.bot.wait_for('reaction_add', timeout=240, check=check_group)
                                except asyncio.TimeoutError:
                                    start = True
                                    break
                                else:
                                    if reaction.emoji == "❌" and sender.id == ctx.author.id:
                                        await ctx.send(f"{ctx.author.mention}'s raid was canceled")
                                        start = False
                                        break
                                    elif reaction.emoji == "✅" and ctx.author.id in group:
                                        sender_user = get_user(sender.id)
                                        if "pet" in sender_user:
                                            if "raid" not in sender_user or not sender_user["raid"]["end_time"] > time.time():
                                                if sender.id not in group:
                                                    group.append(sender.id)
                                                    await ctx.send(f"{sender.mention} Has joined the raid!")
                                            else:
                                                await ctx.send(f"{sender.mention} You already have an ongoing raid")
                                        else:
                                            await ctx.send(f"{sender.mention}You need a pet in order to join a raid, you can buy one with {check_current('prefix')}buypet")
                                    elif reaction.emoji == "⏯" and sender.id == ctx.author.id:
                                        start = True
                                        break
                            if start:
                                reward = int((raids[difficulty.emoji]["coinz"] + random.randint(0, raids[difficulty.emoji]["addition_potential"])) * (len(group) * .3))
                                for user in group:
                                    check_user = get_user(user)
                                    if "raid" not in check_user or not check_user["raid"]["end_time"] > time.time():
                                        start_raid(user, raids[difficulty.emoji]["time"], reward)
                                await ctx.send(f"{ctx.author.mention}'s raid has started!")

                        elif reaction.emoji == "❌":
                            start_raid(ctx.author.id, raids[difficulty.emoji]["time"], raids[difficulty.emoji]["coinz"] + random.randint(0, raids[difficulty.emoji]["addition_potential"]))
                            await ctx.send(f"{ctx.author.mention}'s {user['pet']['emote']} {user['pet']['name']} has sent off on a quest for {seconds_to_readable(raids[difficulty.emoji]['time'])} for up to {raids[difficulty.emoji]['coinz'] + raids[difficulty.emoji]['addition_potential']} coinz")
            else:
                await ctx.send(f"{user['pet']['emote']} {user['pet']['name']} is already in a raid")
        else:
            await ctx.send(f"You need a pet in order to do this, you can buy one with {check_current('prefix')}buypet")


def setup(bot):
    bot.add_cog(Currency(bot))
