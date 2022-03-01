from aiogram.types import \
    ReplyKeyboardMarkup, \
    KeyboardButton


def main():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton('Магазин'), KeyboardButton('Корзина'))
    m.row(KeyboardButton('Кабинет'), KeyboardButton('Помощь'))
    return m
