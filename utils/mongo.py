import pymongo
import os
import time

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

userdata = client["userdata"]
discorduserdata = userdata["discorduserdata"]
discordguilddata = userdata["discordguilddata"]


def get_user(id):
    user = discorduserdata.find_one(id)
    if user:
        return user
    else:
        user = {"_id": id, "coinz": 0, "last_faucet": 0}
        discorduserdata.insert_one(user)
        return user


def get_coinz(id):
    return get_user(id)["coinz"]


def change_coinz(id, amount):
    user = get_user(id)
    new_value = user["coinz"] + amount
    discorduserdata.update_one(user, {"$set": {"coinz": new_value}})
    return new_value


def set_coinz(id, amount):
    user = get_user(id)
    discorduserdata.update_one(user, {"$set": {"coinz": amount}})


def faucet(id, amount, cooldown):
    user = get_user(id)
    if user["last_faucet"] + cooldown < time.time():
        new_balence = user["coinz"] + amount
        discorduserdata.update_one(user, {"$set": {"last_faucet": int(str(time.time()).split(".")[0]), "coinz": new_balence}})
        return [True, new_balence]
    else:
        return [False, user["last_faucet"] + cooldown - int(str(time.time()).split(".")[0])]


def get_guild(id):
    guild = discordguilddata.findone(id)
    if guild:
        return guild
    else:
        guild = {"_id": id, "admin_roles": ["Admins", "Mod"], "reward_roles": {}, "cross_guild_coinz": True}
        discordguilddata.insert_one(guild)
        return guild


def set_guild_settings(id, setting_dict):
    guild = get_guild(id)
    discorduserdata.update_one(guild, {"$set": setting_dict})


def change_guild_admins_list(id, role, boolean):
    pass
