import pymongo
import os
import time

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

userdata = client["userdata"]
discorduserdata = userdata["discorduserdata"]


def get_user(id):
    user = discorduserdata.find_one(id)
    if user:
        return user
    else:
        user = {"_id": id, "coinz": 0, "last_faucet": 0}
        discorduserdata.insert_one(user)
        return user


def set_user_from_dict(dict, new_values_dict):
    discorduserdata.update_one(dict, {"$set": {new_values_dict}})


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

# todo:Themi make it is last faucet var is stored as full seconds without a decemal


def faucet(id, amount, cooldown):
    user = get_user(id)
    if user["last_faucet"] + cooldown < time.time():
        new_balence = user["coinz"] + amount
        discorduserdata.update_one(user, {"$set": {"last_faucet": int(str(time.time()).split(".")[0]), "coinz": new_balence}})
        return [True, new_balence]
    else:
        return [False, user["last_faucet"] + cooldown - int(str(time.time()).split(".")[0])]
