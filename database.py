from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client['anti_gcast_db']

def add_to_blacklist(word):
    db.blacklist.insert_one({"word": word})

def remove_from_blacklist(word):
    db.blacklist.delete_one({"word": word})

def is_blacklisted(word):
    return db.blacklist.find_one({"word": word})

def add_group(group_id, duration):
    db.groups.insert_one({"group_id": group_id, "duration": duration})

def remove_group(group_id):
    db.groups.delete_one({"group_id": group_id})

def get_active_groups():
    return db.groups.find()

def add_user_to_blacklist(user_id):
    db.global_blacklist.insert_one({"user_id": user_id})

def remove_user_from_blacklist(user_id):
    db.global_blacklist.delete_one({"user_id": user_id})

def get_blacklisted_users():
    return db.global_blacklist.find()
