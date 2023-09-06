from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

BLIZZ   = 1287864142
YUNIOR  = 819480320
JR      = 1498420293

SPECIAL_CHARS = ['_', '*', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

TOKEN_NAME = ["🪙", "💎"]

GROUP_ID = '@test_blizzbot_group'
GROUP_LINK = "https://t.me/test_blizzbot_group"

BOT_LINK = "https://t.me/test_promblizzbot?start"

STD_MK = MARKDOWN = "Markdown"

SPAM_MSG = "Usted debera compartir 🔀 las siguientes publicaciones 📳 en diferentes grupos 👥 _cada uno con mas de_ *150* 👤 _usuarios_ y pasar captura 🖼️ de su publicacion y la cantidad de miembros 👥 que tenga el grupo, o de preferencia, una captura donde se pueda visualizar ambas coasas😁👌, una vez el bot 🤖 haya validado sus fotos🔎, recibira un mensaje 📩 de respuesta avisandole, por favor envie varias fotos 📸 como prueba de sus publicaciones😊👍"

BOT_NAME = "PromBOT"

STD_NET = "Por favor, elija una de las siguientes opciones🔖 y le daré las instrucciones📄 de que hacer"

BUILDING = "🚧Under Construction!!🚧"

ADMINS = [
    BLIZZ,
    YUNIOR,
    JR
]

COMMANDS = [
    'start'
]

CANTIDAD_EXTRAER = "😁👍De acuerdo, diga su cantidad de *{TK}* 💵 a extraer\n\n~ 1{TK} = 1 CUP\n~ 10{TK} = 10 CUP\n\n⚠️❗Minimo a extraer: {MIN}{TK}❗⚠️\n\nSaldo actual: {MANY}{TK}"

BTS = {
    "UPDATE": "Actualizar♻️",
    "YES": "Si, es esta!😃",
    "NO": "No, no lo es😒",
    "INVITE": "📨Invitar a...",
    "FOLLOWERS": "Obtener Seguidores👥",
    "BACK": "🔙Volver",
    "REGLAS": "🗣️📣Reglas📑",
    "MORE_WAYS": "⚠️Mas Opciones⚠️",
    "REFERIDOS": {
        "KEY": "👤Referidos👥",
        "GET": "👥Ver Referidos👀",
        "POST": "📎Invitar Referidos🖇️"
    },
    "MONEY": {
        "KEY": "💹Dinero💸",
        "GET": "🏦Extraer Dinero🧾",
        "POST": "🪙Ganar Dinero💰"
    },
    "INLINE": {
        "ACTIVATE": "Activarme",
        "SUB": "Subscribirse📲",
        "CODE": "Escribir código ✍🏻",
        "COMENT": "Comentar",
        "ACCEPT": "Aceptar",
        "DENY": "Banear",
        "FOLLOW": "Seguir",
        "REELS": "Escribir código✍🏻",
        "PAGO": "Avisar de pago",
        "MORE": "🥲Mostrar mas💸",
        "UPDATE": "Actualizar informacion",
        "BOT": "Bots",
        "SPAM": "Publicaciones",
        "SEND_PHOTO": "😶¿Como hago esto?🤔",
        "REMOVE": "❌Borrar Entrada🚮"
    },
    "NET": {
        "IG": "Instagram 🟪",
        "YT": "Youtube 🔴",
        "TLGM": "Telegram 🔵",
        "WHTS": "Whatsapp 🟩"
    },
    "RIFAS": {
        "KEY": "Rifas🔊",
        "GET": "Obtener Informacion📩",
        "POST": "Participar en Rifa🏷️"
    },
    "NO_CODE": "No Tengo un Codigo 😢",
    "CANCEL": "🚫Cancelar🚫"
}

BTNS = {
    "START": [
            [BTS['FOLLOWERS']],
            ["{user}", BTS['REFERIDOS']['KEY']],
            [BTS['MONEY']['GET'], BTS['MONEY']['POST']],
            [BTS['RIFAS']['KEY']],
            [BTS['REGLAS']]
        ],
    "RIFA": [
        [BTS['RIFAS']['GET'], BTS['RIFAS']['POST']],
        [BTS['BACK']]
    ],
    'GRUPO':[[
                InlineKeyboardButton(text="🤖Ir al Privado!😉", url=BOT_LINK)
            ]],
    'EXTRACT': [[BTS['CANCEL']]]
    
}

MESSAGES = {
    "WARNS": {
        "MSG": [
            "🪬Advertencia {}/3, a partir de la 3era comenzaremos a descontar tokens❌🏆\n\nLos posibles motivos por los que se haya rechazado🪬su prueba 📧, pueden verlos pulsando 👉 /rules 👈 o mirando el apartado de \"reglas\"📋 en el menú principal🗄",
            "Advertencia {}/3, hemos descontado {} de sus {}"
        ]
    },
    "EXTRACT": {
        'MARKDOWN': STD_MK,
        "BTN": ReplyKeyboardMarkup(BTNS['EXTRACT'], True),
        "MSG": [
            "`{}` no es una direccion valida 😕, por favor, introduzca una direccion🪪 a la que podamos enviar su dinero 💵 (Numero de telefono📱 o Tarjeta de Banco 💳)",
            "🚫Usted no tiene saldo 💳 suficiente para hacer la extracción 💵 solicitada.\nSu saldo actual es de: {} {}❗",
            "🥺Su solicitud esta siendo procesada por los 🤵🏻‍♂️admin, por favor espere...👨🏻‍💻",
            '⚠️Debe tener al menos {LIMIT_B} {TK_N}❗ para efectuar el pago\n\nEsto significa que usted debera tener en su cuenta 💳 al menos {LIMIT_B} {TK_N} para efectuar el pago.⚠️\n\n💳Su cantidad actual es de: {MANY}',
            'Por favor, vuelva a especificar la direccion 💳 de destino de su cuenta 🪪',
            "Usted ha introducido *{}*🪪 como nuevo destino, este correcto?🤔"
        ]
    },
    "SEND": {
        'MARKDOWN': STD_MK,
        "BTN": None,
        "MSG": [
            "😢No se ha detectado una foto, por favor, reenviela📨",
            "Su pago 💵 ha sido enviado a su destino📨, por favor espere paciente a recibirlo😁👍"
        ]
    },
    "PROOFS": {
        'MARKDOWN': STD_MK,
        "BTN": None,
        "MSG": [
            "Enviadas sus pruebas 📪a los admin, espere 👁‍🗨 respuesta…. ",
            "Su foto 🌁 se agrego 📲satisfactoriamente👌, por favor, envie 👉🏻{CMD} para detener el envio de fotos🪬",
        ]
    },
    'REDES': {
        'MARKDOWN': STD_MK,
        "MSG": [
            "😃Estas son las redes 🕸️ que tenemos en este momento👨‍💻",
            "😢No tenemos redes 🕸️ para seguir en este momento👨‍💻",
            "😃Estos son los bots 🤖 que tenemos en este momento👨‍💻",
            "😢No tenemos bots 🤖 para para acceder en este momento👨‍💻"
        ],
        "BTN": None
    },
    'GROUP': {
        'MARKDOWN': STD_MK,
        'BTN': BTNS['GRUPO'],
        'MSG': [
            "Hola {USER}, bienvenido!😄 Pasate por mi privado 🕵️‍♂️ si quieres hacer un dinerito 💹 extra ;)\n\n*ES GRATIS!*😉",
            '{USER} ha abandonado el grupo👥, pero lo recordare📲 x si aun desea volver 😢',
            'Agradecimientos especiales 😄 para `{INVITER}` por haber invitado 📨 a `{USER}` al grupo 🤗'
            ]
    },
    "REGLAS": {
        "MARKDOWN": STD_MK,
        "MSG": [
            "Mensaje de reglas que me debe dar el jhonny"
        ],
        "BTN": None
    },
    "START": {
        "MARKDOWN": None,
        "MSG": [
            "Bienvenido {user}, soy PromBOT 🖲 ¿En qué te puedo ayudar? 👀👇🏻\nAquí están mis comandos📃\n.Te ayudaremos a ganar dinero💵 y seguidores👥.",
            "Bienvenido de vuelta🖲, {user}!\nQué desea?👁‍🗨",
            "❌No se reconoce su entrada 📲"
        ],
        "BTN": BTNS['START']
    },
    "YT": {
        "MARKDOWN": None,
        "MSG": [STD_NET],
        "BTN": InlineKeyboardMarkup([[InlineKeyboardButton(text=BTS['INLINE']['SUB'], callback_data=BTS['INLINE']['SUB']),InlineKeyboardButton(text=BTS['INLINE']['CODE'], callback_data=BTS['INLINE']['CODE'])]]),
        "INST": {
            "SUB": f"Para empezar a ganar dinero 💵 deberás subscribirte🔔 y subir una captura de pantalla📱 para verificar que has realizado la acción✅.\n\nEl bot 🖲lo revisará.\n\nLa recompensa 🪙 por subscribirse es un {TOKEN_NAME[1]} ",
            "CODE": f"En los videos 🖥 aparecen diversos códigos ⭕️ en la parte inferior derecha del video.\n\nDebes escribirlos ✍🏻 para recibir un {TOKEN_NAME[1]} por código."
        }
    },
    "IG": {
        "MARKDOWN": None,
        "MSG": [STD_NET],
        "BTN": InlineKeyboardMarkup([[InlineKeyboardButton(text=BTS['INLINE']['FOLLOW'], callback_data=BTS['INLINE']['FOLLOW']),InlineKeyboardButton(text=BTS['INLINE']['REELS'], callback_data=BTS['INLINE']['REELS'])], [InlineKeyboardButton(BTS['INLINE']['COMENT'], callback_data=BTS['INLINE']['COMENT'])]]),
        "INST": {
            "FOLLOW": "Siga las siguientes cuentas de instagram📷 y suba una captura de pantalla 🖼️ para probar su validez, una ves haya verificado ✅ esto, se le informara.📫",
            "REELS": "Los siguientes reels de instagram tienen códigos ⭕️ en algún punto del video 🖥, escríbalo ✍🏻 según lo encuentre para ganar tokens🏆",
            "COMENT": "Comenta y dale LIKE 👍 a este reel/post 😁 de instagram📷 y toma una captura de pantalla🖼️, una vez hecho esto, sube la captura📤 y el bot procedera a validarla📨"
        }
    },
    "TLGM": {
        "MARKDOWN": STD_MK,
        "MSG": [STD_NET],
        "BTN": InlineKeyboardMarkup([[
            InlineKeyboardButton(BTS['INLINE']['SPAM'], callback_data=BTS['INLINE']['SPAM']), InlineKeyboardButton(BTS['INLINE']['BOT'], callback_data=BTS['INLINE']['BOT'])
        ]]),
        "INST": {
            "BOT": "😃Los siguientes 🤖bots son parecidos a este, 😱¡con ellos tambien podras hacer un dinero extra!😉",
            "SPAM": SPAM_MSG
        }
    },
    "WHTS": {
        "MARKDOWN": STD_MK,
        "MSG": [STD_NET],
        "BTN": InlineKeyboardMarkup([[
            InlineKeyboardButton(BTS['INLINE']['SPAM'], callback_data=BTS['INLINE']['SPAM'])
        ]]),
        "INST": {
            "SPAM": SPAM_MSG
        }
    },
    "MORE_WAYS": {
        "MARKDOWN": STD_MK,
        "MSG": [f"Otras formas de ganar 💹 es invitando usuarios 👤 a usar el 🤖bot, ¿Como? ¡Pues fácil! 🍼👶 Usted deberá ir a su apartado de referidos 👥 y hacer click en invitar, recibirá un link ⛓️ de referido, el cual deberá compartir 📬 con sus amigos y familiares 👨‍👩‍👧‍👦 para que estos se refieran a usted, ganara 1 {TOKEN_NAME[1]} por cada referido y sus invitados entrarán con 2 {TOKEN_NAME[1]}, ¡Todos Ganan usando {BOT_NAME}!😃"],
        "BTN": None
    },
    "INVALID_CODE": {
        "MARKDOWN": None,
        "MSG": ["📜Por favor introduzca un codigo valido!📝"],
        "BTN": ReplyKeyboardMarkup([[BTS['NO_CODE']]], resize_keyboard=True)
    },
    "NO_CODE": {
        "MARKDOWN": None,
        "MSG": ["😁De acuerdo, desea hacer algo mas?😊"],
        "BTN": None
    },
    "RIFAS": {
        "MARKDOWN": None,
        "MSG": ["👁‍🗨Veo que estas interesado en las rifas💎, que bien!!"],
        "BTN": ReplyKeyboardMarkup(BTNS['RIFA'], resize_keyboard=True)
    }
}

def format_mk(text: str):
    for char in SPECIAL_CHARS:
        escaped_char = '\\' + char
        text = text.replace(char, escaped_char)
    return text


def unformat_mk(text: str):
    return text.replace('\\', '')

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
            btns = [ ] # MESSAGES[key]['BTN']
            for i, v in enumerate(MESSAGES[key]['BTN']):
                btns.append([])
                for j in v:
                    # print(f"\t{i}\t{j}\t{kargs['user']}")
                    btns[i].append(j.format(user=f"👤 {kargs['user']} 📑"))
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
    

    