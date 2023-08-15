from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

BLIZZ   = 1287864142
YUNIOR  = 819480320
JR      = 1498420293

TOKEN_NAME = ["A", "B"]

GROUP_ID = '@test_blizzbot_group'


ADMINS = [
    BLIZZ,
    YUNIOR,
    JR
]

COMMANDS = [
    'start'
]

CANTIDAD_EXTRAER = "De acuerdo, diga su cantidad de *{TK}* a extraer\n\n~ 1{TK} = 1 CUP\n~ 10{TK} = 10 CUP\n\nMinimo a extraer: 10{TK}"

BTS = {
    "YES": "Si, es esta!",
    "NO": "No, no lo es",
    "INVITE": "Invitar a...",
    "FOLLOWERS": "Obtener Seguidores",
    "BACK": "Volver",
    "REFERIDOS": {
        "KEY": "Referidos",
        "GET": "Ver Referidos",
        "POST": "Invitar Referidos"
    },
    "MONEY": {
        "KEY": "Dinero",
        "GET": "Extraer Dinero",
        "POST": "Ganar Dinero"
    },
    "INLINE": {
        "ACTIVATE": "Activarme",
        "SUB": "Subscripciones",
        "CODE": "Insertar Codigo",
        "ACCEPT": "Aceptar",
        "DENY": "Banear",
    },
    "NET": {
        "IG": "Instagram",
        "YT": "YouTube"
    },
    "RIFAS": "Participar en Rifa!!",
    "NO_CODE": "No Tengo un Codigo :("
}

MESSAGES = {
    "START": {
        "MARKDOWN": None,
        "MSG": "Bienvenido a {user}!\nElija una opcion:",
    },
    "YT": {
        "MARKDOWN": None,
        "MSG": "Mensaje que despues @JRMast me debe dar",
        "BTN": InlineKeyboardMarkup([[InlineKeyboardButton(text=BTS['INLINE']['SUB'], callback_data=BTS['INLINE']['SUB']),InlineKeyboardButton(text=BTS['INLINE']['CODE'], callback_data=BTS['INLINE']['CODE'])]]),
        "INST": {
            "SUB": "Mensaje de instrucciones para cuando se quiera ganar con subs",
            "CODE": "Mensaje de instrucciones para cuando se quiera ganar con codigos"
        }
    },
    "INVALID_CODE": {
        "MARKDOWN": None,
        "MSG": "Por favor introduzca un codigo valido!",
        "BTN": ReplyKeyboardMarkup([[BTS['NO_CODE']]], resize_keyboard=True)
    },
    "NO_CODE": {
        "MARKDOWN": None,
        "MSG": "De acuerdo, desea hacer algo mas?",
    }
}

def get_msg(key, *args, **kargs):
    
    if key == 'START':
        if kargs['user'] is not None:
            mk = MESSAGES[key]['MARKDOWN']
            msg = MESSAGES[key]['MSG'].format(user=kargs['user'])
            btns = [
                [BTS['FOLLOWERS']],
                [kargs['user'], BTS['REFERIDOS']['KEY']],
                [BTS['MONEY']['GET'], BTS['MONEY']['POST']],
                [BTS['RIFAS']]
            ]
            return {
                "MARKDOWN": mk,
                "MSG": msg,
                "BTN": ReplyKeyboardMarkup(btns, resize_keyboard=True)
            }
        else:
            raise Exception("No se ha seleccionado un usuario")
    else:
        return MESSAGES[key]
    

    