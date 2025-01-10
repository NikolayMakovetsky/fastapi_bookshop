import json

from api.core.logging import logger

translations = {}
supported_langs = ['en', 'ru']
default_language = 'en'


def load_localize_data():
    for lang in supported_langs:
        try:
            with open(f'../api/core/resources/localize/messages.{lang}.json', encoding='utf-8') as file:
                data = json.load(file)
                for k, v in data.items():
                    translations[(lang, k)] = v
        except:
            logger.error(f'ERROR: File "../core/resources/localize/messages.{lang}.json" not found.')


def get_localize_text(lang: str, msg_key: str) -> str:
    """
    Функция возвращает локализационное сообщение
    из локализационного словаря translations, соответствующее
    передаваемому языку и ключу сообщения

    :param lang: язык локали
    :param msg_key: ключ сообщения
    :return: локализационное сообщение

    Рекомендуется применять alias при импорте функции:
    import get_localize_text as _
    """
    msg_str = translations.get((lang, msg_key), "")
    return msg_str
