BLIZZ = 1287864142
TOKEN_NAME = ["Token", "token_b"]

ADMINS = [
    BLIZZ
]

COMMANDS = [
    'start'
]



BTS = {
    "INFO": "Mi informacion",
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
        "ACTIVATE": "Activarme"
    },
    "NET": {
        "IG": "Instagram",
        "YT": "YouTube"
    }
}

def get_msg(key, *args, **kargs):
    MESSAGES = {
        "START": {
            "MARKDOWN": None,
            "MSG": "Bienvenido a {user}!\nElija una opcion:",
        }
    }
    mk = MESSAGES[key]['MARKDOWN']
    if kargs['user'] is not None and key == 'START':
        msg = MESSAGES[key]['MSG'].format(user=kargs['user'])
        btns = [
            [BTS['FOLLOWERS']],
            [kargs['user'], BTS['REFERIDOS']['KEY']],
            [BTS['MONEY']['GET'], BTS['MONEY']['POST']]
        ]
        return {
            "MARKDOWN": mk,
            "MSG": msg,
            "BTN": btns
        }
    elif kargs['user'] is None and key == 'START':
        raise Exception("No se ha seleccionado un usuario")
