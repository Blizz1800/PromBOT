from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

BLIZZ   = 1287864142
YUNIOR  = 819480320
JR      = 1498420293

TOKEN_NAME = ["A", "B"]

GROUP_ID = '@test_blizzbot_group'

MARKDOWN = "Markdown"

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
        "COMENT": "Comentarios",
        "ACCEPT": "Aceptar",
        "DENY": "Banear",
        "FOLLOW": "Siguiendo",
        "REELS": "Ver Reels",
        "PAGO": "Avisar de pago",
        "MORE": "🥲Mostrar mas💸",
        "UPDATE": "Actualizar informacion",

    },
    "NET": {
        "IG": "Instagram",
        "YT": "YouTube"
    },
    "RIFAS": {
        "KEY": "Rifas",
        "GET": "Obtener Informacion",
        "POST": "Participar en Rifa"
    },
    "NO_CODE": "No Tengo un Codigo :(",
    "CANCEL": "Cancelar"
}

BTNS = {
    "START": [
            [BTS['FOLLOWERS']],
            ["{user}", BTS['REFERIDOS']['KEY']],
            [BTS['MONEY']['GET'], BTS['MONEY']['POST']],
            [BTS['RIFAS']['KEY']]
        ],
    "RIFA": [
        [BTS['RIFAS']['GET'], BTS['RIFAS']['POST']],
        [BTS['BACK']]
    ]
    
}

MESSAGES = {
    "START": {
        "MARKDOWN": None,
        "MSG": [
            "Bienvenido {user}!\nQue desea?",
            "Bienvenido de vuelta, {user}!\nQue desea?",
            "No se reconoce su entrada"
        ],
        "BTN": BTNS['START']
    },
    "YT": {
        "MARKDOWN": None,
        "MSG": ["Mensaje que despues @JRMast me debe dar"],
        "BTN": InlineKeyboardMarkup([[InlineKeyboardButton(text=BTS['INLINE']['SUB'], callback_data=BTS['INLINE']['SUB']),InlineKeyboardButton(text=BTS['INLINE']['CODE'], callback_data=BTS['INLINE']['CODE'])]]),
        "INST": {
            "SUB": "Mensaje de instrucciones para cuando se quiera ganar con subs",
            "CODE": "Mensaje de instrucciones para cuando se quiera ganar con codigos"
        }
    },
    "IG": {
        "MARKDOWN": None,
        "MSG": ["Mensaje que despues @JRMast me debe dar"],
        "BTN": InlineKeyboardMarkup([[InlineKeyboardButton(text=BTS['INLINE']['FOLLOW'], callback_data=BTS['INLINE']['FOLLOW']),InlineKeyboardButton(text=BTS['INLINE']['REELS'], callback_data=BTS['INLINE']['REELS'])], [InlineKeyboardButton(BTS['INLINE']['COMENT'], callback_data=BTS['INLINE']['COMENT'])]]),
        "INST": {
            "FOLLOW": "Mensaje de instrucciones para cuando se quiera ganar con seguimiento",
            "REELS": "Mensaje de instrucciones para cuando se quiera ganar viendo reels",
            "COMENT": "Mensaje de instrucciones para cuando se quiera ganar con comentarios, por favor envie varias fotos como prueba de sus publicaciones"
        }
    },
    "INVALID_CODE": {
        "MARKDOWN": None,
        "MSG": ["Por favor introduzca un codigo valido!"],
        "BTN": ReplyKeyboardMarkup([[BTS['NO_CODE']]], resize_keyboard=True)
    },
    "NO_CODE": {
        "MARKDOWN": None,
        "MSG": ["De acuerdo, desea hacer algo mas?"],
        "BTN": None
    },
    "RIFAS": {
        "MARKDOWN": None,
        "MSG": ["Veo q estas interesado en las rifas, que bien!!"],
        "BTN": ReplyKeyboardMarkup(BTNS['RIFA'], resize_keyboard=True)
    }
}

def get_msg(key, *args, **kargs):
    v = 0
    if ':' in key:
        key, v = tuple(key.split(':'))
    try:
        v = int(v) -1 
    except ValueError:
        v = 0
    if key == 'START':
        if kargs['user'] is not None or len(args) > 0 and args[0] is not None:
            mk = MESSAGES[key]['MARKDOWN']
            msg = MESSAGES[key]['MSG'][v].format(user=kargs['user'])
            btns = MESSAGES[key]['BTN']
            for i, v in enumerate(btns):
                for i2, j in enumerate(v):
                    btns[i][i2] = j.format(user=kargs['user'])
            return {
                "MARKDOWN": mk,
                "MSG": msg,
                "BTN": ReplyKeyboardMarkup(btns)
            }
        else:
            raise Exception("No se ha seleccionado un usuario")
    else:
        result = { }
        msg = MESSAGES[key]
        for k in msg.keys():
            if k == 'MSG':
                result[k] = msg[k][v]
                continue
            result[k] = msg[k]
        return result
    

    