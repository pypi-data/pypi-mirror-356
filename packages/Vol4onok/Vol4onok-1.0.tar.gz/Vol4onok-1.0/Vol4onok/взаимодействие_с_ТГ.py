# pip install pytz
# pip install python-dotenv
# pip install python-telegram-bot==13.7

import os
import time
from datetime import datetime
from pytz import UTC
from telegram import Bot

RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
BLUE = '\x1b[34m'
RESET = '\x1b[39m'

ТОКЕН = None
БОТ = None
эта_папка = os.path.dirname(__file__)

def __check_token(токен):
    if not токен:
        raise ValueError(RED + 'ТГ токен не обнаружен' + RESET)

def загрузить_токен(токен):
    __check_token(токен)
    global ТОКЕН
    global БОТ
    ТОКЕН = токен
    try:
        БОТ = Bot(ТОКЕН)
        return True
    except:
        print(RED + "Токен некорректный, либо нет интернета" + RESET)
        return False

def отправить_сообщение(сообщение: str, айди: str, кнопки=None):
    if type(айди) == str and not айди.isnumeric():
        if not type(сообщение) == bytes:
            print(BLUE + f"{сообщение}" + RESET)
        else:
            print(YELLOW + f"->  картинка" + RESET)
        return

    айди = int(айди)
    __check_token(ТОКЕН)
    try:
        БОТ.send_message(chat_id=айди, text=сообщение, reply_markup=кнопки)
        if not type(сообщение) == bytes:
            print(YELLOW + f"->  {сообщение}" + RESET)
        else:
            print(YELLOW + f"->  картинка" + RESET)
    except Exception as error:
        print(f"Возникла ошибка {RED}{error}{RESET}")

def отправить_картинку(ссылка: str, айди: str, кнопки=None):
    if type(айди) == str and not айди.isnumeric():
        if not type(ссылка) == bytes:
            print(BLUE + f"{ссылка}" + RESET)
        else:
            print(YELLOW + f"->  картинка" + RESET)
        return

    айди = int(айди)
    __check_token(ТОКЕН)
    try:
        БОТ.send_photo(chat_id=айди, photo=ссылка, reply_markup=кнопки)
        if not type(ссылка) == bytes:
            print(YELLOW + f"->  {ссылка}" + RESET)
        else:
            print(YELLOW + f"->  картинка" + RESET)
    except Exception as error:
        print(f"Возникла ошибка {RED}{error}{RESET}")

def проверить_входящие(айди=None, максимальное_ожидание_ответа_в_секундах=None):
    if айди:
        if not айди.isnumeric():
            raise ValueError(RED + f"неподдерживаемый формат айди: {айди}" + RESET)
        айди = int(айди)

    __check_token(ТОКЕН)
    def отмена_если_нет_ответа(now):
        if максимальное_ожидание_ответа_в_секундах and (datetime.now(UTC) - now).seconds > максимальное_ожидание_ответа_в_секундах:
            print(f"Не было ответа в течении {максимальное_ожидание_ответа_в_секундах} сек. Перестаём следить за этим юзером")
            return True

    def создать_last_msg(update_id):
        with open(f'{эта_папка}\\last_msg', 'w', encoding='utf-8') as file:
            file.write(str(update_id))

    def считать_last_msg():
        with open(f'{эта_папка}\\last_msg', 'r', encoding='utf-8') as file:
            return int(file.read())

    now = datetime.now(UTC)
    if not os.path.exists(f'{эта_папка}\\last_msg'):
        while True:
            try:
                обновления = БОТ.get_updates()
                if отмена_если_нет_ответа(now):
                    return None
                if not обновления:
                    time.sleep(0.5)
                    continue
                break
            except:
                continue
        last_msg = обновления[-1]
        if last_msg.message.date < now:
            создать_last_msg(last_msg.update_id)
        else:
            создать_last_msg(last_msg.update_id - 1)

    while True:
        if отмена_если_нет_ответа(now):
            return None
        try:
            обновления = БОТ.get_updates(offset=считать_last_msg() + 1)
        except:
            time.sleep(1)
            continue
        if not обновления:
            continue

        обновления.reverse()
        # print(len(обновления))
        for msg in обновления:
            if айди is None or msg.effective_user.id == айди:
                создать_last_msg(msg.update_id)
                print(GREEN + f"⬅️   {msg.effective_message.text}" + RESET)
                return msg
        time.sleep(0.5)
