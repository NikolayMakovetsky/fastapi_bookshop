import json

from api.core.logging import logger

translations = {}
supported_langs = ['en', 'ru']


def load_localize_data():
    for lang in supported_langs:
        try:
            with open(f'../api/core/resources/localize/messages.{lang}.json', encoding='utf-8') as file:
                data = json.load(file)
                for k, v in data.items():
                    translations[(lang, k)] = v
        except:
            logger.error(f'ERROR: File "../core/resources/localize/messages.{lang}.json" not found.')


def get_localize_text(msg_key: str) -> str:
    msg_str = translations.get(('ru', msg_key), "")
    return msg_str
