import pymongo
import os

client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@{os.environ['MONGO_SERVER']}")

db = client["test"]


def mongo_test():
    print(client.list_database_names())
