from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

BLIZZ   = 1287864142
YUNIOR  = 819480320
JR      = 1498420293

TOKEN_NAME = ["A", "B"]

ADMINS = [
    BLIZZ,
    YUNIOR,
    JR
]

COMMANDS = [
    'start'
]


BTS = {
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
        "CODE": "Insertar Codigo"
    },
    "NET": {
        "IG": "Instagram",
        "YT": "YouTube"
    },
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
    

    