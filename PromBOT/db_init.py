from .commands import DB

def db_init_update():
    DB['users'].update_many({"token_a": {"$exists": False}}, {"$set": {"token_a": 0}})
    DB['users'].update_many({"tokens": {"$exists": True}}, {"$rename": {"tokens": "token_b"}})
