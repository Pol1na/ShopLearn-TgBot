from aiogram.types import \
    KeyboardButton, \
    ReplyKeyboardMarkup


def cancel(*, skip=False, request_contact=False):
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    if request_contact:
        m.row(KeyboardButton('Поделиться номером', request_contact=True))
    if skip:
        m.row(KeyboardButton('Пропустить'))
    m.row(KeyboardButton('Отменить'))
    return m


def get_phone():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton('Поделиться номером', request_contact=True))
    return m
