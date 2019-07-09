from discord.ext import commands
from utils.mongo import get_user, get_coinz, change_coinz, set_coinz, faucet, new_pet, battle_results
import random
from utils.makeReadable import array_to_space_list, seconds_to_readable
from utils.options import check_current
import asyncio
import discord

sent_requests = []
pets = ["🐱", "🐭", "🐶", "🐷", "🐮", "🐔", "🦁"]
slots = {":cherries:": {"multiplier": 0, "chance": .01},
         ":bell:": {"multiplier": 8, "chance": .40},
         ":watermelon:": {"multiplier": 6, "chance": .01},
         ":gem:": {"multiplier": 18, "chance": .01},
         ":eggplant:": {"multiplier": 10, "chance": .01},
         ":tangerine:": {"multiplier": 8, "chance": .01}}


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
        if amount > 0:
            coinz = get_coinz(ctx.author.id)
            if amount <= coinz:
                won = False
                reel = []
                cherries = 0
                for emote in slots:
                    if random.random() < slots[emote]["chance"]:
                        for i in range(0, 3):
                            reel[i] = emote
                        win_amount = amount * slots[emote]["multiplier"]
                        won = True
                        break
                print(reel)
                if not won:
                    emotes = list(slots.keys())
                    first_draw = random.choice(emotes)
                    reel.append(first_draw)
                    emotes.remove(first_draw)
                    for i in range(0, 2):
                        reel.append(random.choice(emotes))
                cherries = reel.count(":cherries:")
                print(cherries)
                win_amount = cherries * 3
                if win_amount == 0:
                    message = f"no good :(, lost {win_amount} coinz"
                else:
                    if cherries > 0:
                        if win_amount >= amount:
                            message = f"Got {cherries} cherries and won {coinz}!"
                        else:
                            message = f"Got {cherries} and won {coinz}, but spent {win_amount} on the spin :("
                    else:
                        message = f"Won {win_amount} coinz!"
                change_coinz(ctx.author.id, (-1 * amount) + win_amount)
                await ctx.send(array_to_space_list(reel) + "\n" + message)
            else:
                await ctx.send(f"You don't have enough coinz, you only have {coinz}")
        else:
            await ctx.send("Amount must be more then 0")

        # The old slots code
        # coinz = get_coinz(ctx.author.id)
        # reel = []
        # if amount <= coinz:
        #     if amount > 0:
        #         for i in range(0, 3):
        #             reel.append(random.choice(emojis))
        #         if ":poop:" in reel:
        #             change_coinz(ctx.author.id, -1 * amount)
        #             message = "poopy spin... no win :("
        #         elif reel.count(":cherries:") > 0:
        #             win_amount = reel.count(":cherries:") * 4
        #             change_coinz(ctx.author.id, win_amount - amount)
        #             if win_amount > amount:
        #                 message = f"Got {reel.count(':cherries:')} :cherries: and won {win_amount} coinz!"
        #             else:
        #                 message = f"Got {reel.count(':cherries:')} :cherries: and won {win_amount} coinz, but spent {amount} on the spin"
        #         elif reel[0] == reel[1] and reel[1] == reel[2]:
        #             win_amount = win_amounts[reel[0]] * amount
        #             change_coinz(ctx.author.id, win_amount - amount)
        #             message = f"Won {win_amount + amount} coinz!! Woo!"
        #         else:
        #             change_coinz(ctx.author.id, -1 * amount)
        #             message = f"no win :( lost {amount}"
        #         await ctx.send(array_to_space_list(reel) + "\n" + message)
        #     else:
        #         await ctx.send("You must bet more then 0")
        # else:
        #     await ctx.send(f"You need more coinz, you currently have {coinz} coinz")

    @commands.command()
    async def slotspayouts(self, ctx):
        """Get tempted into playing slots"""
        pass
        # message = "Payout amounts:\n"
        # for emoji, amount in win_amounts.items():
        #     message = message + "\n" + emoji + ": " + str(amount) + "x spin cost"
        # message = message + "\n:cherries:: 3 credits"
        # await ctx.send(message)

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

    @commands.command()
    async def battle(self, ctx, defending: discord.Member, amount: int):
        """Heck someone up and take their coinz gang gang style"""
        if not ctx.author == defending:
            user = get_user(ctx.author.id)
            defending_user = get_user(defending.id)
            min = 10
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
                                        return sender == defending and reaction.emoji in ["✅", "❌"] or sender == ctx.author and reaction.emoji == "❌"

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
                        await ctx.send("The person who you challenged does not have a pet, use +pet to buy one")
                else:
                    await ctx.send("You need a pet to play, use +pet to buy one")
            else:
                await ctx.send(f"You need to bet at least {min} coinz")
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


def setup(bot):
    bot.add_cog(Currency(bot))
