from aiogram.types import \
    ReplyKeyboardMarkup, \
    KeyboardButton


def admin():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton('Магазин'), KeyboardButton('Статистика'))
    return m
