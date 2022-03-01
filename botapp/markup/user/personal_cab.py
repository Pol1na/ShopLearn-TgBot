from aiogram.types import \
    ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup


def personal_cab_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(KeyboardButton('Мои данные'), KeyboardButton('Мои заказы'))
    m.row(KeyboardButton('В главное меню'))
    return m


def edit_user_data(edit=False):
    m = InlineKeyboardMarkup()
    if edit:
        m.row(InlineKeyboardButton('ФИО', callback_data='edit-user-data:fio'),
              InlineKeyboardButton('Номер телефона', callback_data='edit-user-data:phone'))
        m.row(InlineKeyboardButton('Адрес', callback_data='edit-user-data:address'))
        m.row(InlineKeyboardButton('Назад', callback_data='back-to-my-data'))
        return m
    m.row(InlineKeyboardButton('Редактировать', callback_data='edit-my-data'))
    return m
