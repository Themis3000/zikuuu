import pymongo
import os

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

userdata = client["userdata"]
discorduserdata = userdata["discorduserdata"]


def get_user(id):
    user = discorduserdata.find_one(id)
    if user:
        return user
    else:
        user = {"_id": id, "coinz": 0}
        discorduserdata.insert_one(user)
        return user


def get_coinz(id):
    return get_user(id)["coinz"]


def change_coinz(id, amount):
    user = get_user(id)
    discorduserdata.update_one(user, {"$set": {"coinz": user["coinz"] + amount}})


def set_coinz(id, amount):
    user = get_user(id)
    discorduserdata.update_one(user, {"$set": {"coinz": amount}})
