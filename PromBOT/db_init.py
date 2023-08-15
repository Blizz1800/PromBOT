from .commands import DB

def db_init_update():
    DB['users'].update_many({"token_a": {"$exists": False}}, {"$set": {"token_a": 0}})
    DB['users'].update_many({"tokens": {"$exists": True}}, {"$rename": {"tokens": "token_b"}})
    DB['users'].update_many({"banned": {"$exists": False}}, {"$set": {"banned": False}})
    DB['users'].update_many({'target': {"$exists": False}}, {"$set": {"target": None}})