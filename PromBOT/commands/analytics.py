from . import get_db
# from bson import ObjectId
from enum import Enum

DB = get_db('analytics')


class TK_RED(Enum):
    YOUTUBE_CODES = 'youtube_codes'
    YOUTUBE_SUB = 'youtube_sub'
    REFERIDOS = 'referidos'
    INSTAGRAM_REEL = 'inst_reel'
    INSTAGRAM_COM = 'inst_com'
    INSTAGRAM_FOLL = 'inst_foll'

class TK(Enum):
    A = 'tk_a'
    B = 'tk_b'

def earn_tk(TK_RED: str, uid: int | str, many: int, tk: TK = TK.B):
    global DB
    target_db = DB['tokens']
    if not target_db.find_one({'red': TK_RED}):
        target_db.insert_one({
            'red': TK_RED,
            'tk_a': 0,
            'tk_b': 0,
            'users': [
                {
                    'uid': uid,
                    'tk_a': 0,
                    'tk_b': 0
                }
            ]
        })
    if not target_db.find_one({ 'red': TK_RED, "users.uid": uid }):
        target_db.update_one({ 'red': TK_RED,}, {"$push": {'users': {'uid': uid, 'tk_a': 0, 'tk_b': 0}}})
    
    target_db.update_one(
        {
            'red': TK_RED,
            "users.uid": uid
        },
        {
            '$inc': {
                tk: many,
                f'users.$.{tk}': many
            }
        }
    )
    result = target_db.find_one({'red': TK_RED, "users.uid": uid}, {tk: 1, f'users.$.{tk}': 1})
    return ({'tk_a': result['tk_a'], 'tk_b': result['tk_b']}, {'tk_a': result['users.$.tk_a'], 'tk_b': result['users.$.tk_b']})



def button_press(btn: str, uid: int, inline: bool = False) -> tuple([int, int]):
    # usr = DB['users'].find_one({'t_id': uid})
    global DB
    target_db = DB['buttons']
    if not target_db.find_one({'btn': btn}):
        target_db.insert_one({
            'btn': btn,
            'inline': inline,
            'times': 0,
            'users': [
                {
                    "uid": uid,
                    "times": 0
                }
            ]
        })
    if not target_db.find_one({ 'btn': btn, "users.uid": uid }):
        target_db.update_one({ 'btn': btn,}, {"$push": {'users': {'uid': uid, 'times': 0}}})
    target_db.update_one(
        {
            'btn': btn,
            "users.uid": uid
        },
        {
            '$inc': {
                'times': 1,
                'users.$.times': 1
            }
        }
    )
    result = target_db.find_one({'btn': btn, "users.uid": uid}, {'times': 1, 'users.$': 1})
    u_times = result['users'][0]['times']
    return tuple([result['times'], u_times])
