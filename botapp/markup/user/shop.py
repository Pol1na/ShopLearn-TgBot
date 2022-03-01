from aiogram.types import \
    ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup


def user_categories(categories_data, what_need, page=1, parent_id=None):
    m = InlineKeyboardMarkup(resize_keyboard=True)
    item_on_page = 8
    if what_need == 'showproduct':
        for category in categories_data[(int(page) * item_on_page) - item_on_page:int(page) * item_on_page]:
            print(category)
            m.row(InlineKeyboardButton(text=category['name'],
                                       callback_data=f"shop_menu:{what_need}:{category['product_id']}"))
    else:
        for category in categories_data[(int(page) * item_on_page) - item_on_page:int(page) * item_on_page]:
            print(category)
            m.row(InlineKeyboardButton(text=category['name'],
                                       callback_data=f"shop_menu:{what_need}:{category['category_id']}"))
    # !!!
    if parent_id is not None:
        m.row(InlineKeyboardButton(text='Назад', callback_data=f'back-to-category:{parent_id}'))

    m.row(InlineKeyboardButton(text='<', callback_data=f"pagination:{what_need}:{parent_id}:{int(page) - 1}"),
          InlineKeyboardButton(text='>', callback_data=f"pagination:{what_need}:{parent_id}:{int(page) + 1}"))

    return m


def gen_subaddtocart_menu(product_id):
    m = InlineKeyboardMarkup(resize_keyboard=True)
    add_to_cart = InlineKeyboardButton(text='Добавить в корзину', callback_data=f'subadd_cart:{product_id}')
    back_btn = InlineKeyboardButton(text='Назад', callback_data=f'back_btn')
    m.add(add_to_cart)
    m.add(back_btn)
    return m


def gen_add_to_cart(product_id, number=1):
    add_to_cart_menu = InlineKeyboardMarkup(resize_keeyboard=True)
    add = InlineKeyboardButton(text='Добавить', callback_data=f'add_cart:{number}:{product_id}')
    minus = InlineKeyboardButton(text='-', callback_data=f'amount_minus:{number}:{product_id}')
    amount = InlineKeyboardButton(text=f'{number}', callback_data=f'amount:{number}:{product_id}')
    plus = InlineKeyboardButton(text='+', callback_data=f'amount_plus:{number}:{product_id}')
    add_to_cart_menu.add(add)
    add_to_cart_menu.add(minus, amount, plus)
    back_btn = InlineKeyboardButton(text='Назад', callback_data=f'back_btn')
    add_to_cart_menu.add(back_btn)
    return add_to_cart_menu


def user_cart():
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton('Оформить заказ', callback_data='form-order'))
    m.row(InlineKeyboardButton('Очистить корзину', callback_data='clear-cart'))
    return m


def use_data():
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton('Да, использовать эти', callback_data='use_this_data:yes'))
    m.row(InlineKeyboardButton('Нет, указать другие', callback_data='use_this_data:no'))
    return m


def check_save_data():
    m = InlineKeyboardMarkup()
    m.row(InlineKeyboardButton('Да, сохранить', callback_data='save-new-order-data:yes'))
    m.row(InlineKeyboardButton('Нет, не сохранять', callback_data='save-new-order-data:no'))
    return m


def payments(payments):
    m = InlineKeyboardMarkup()
    for payment in payments:
        m.row(InlineKeyboardButton(f"{payment['payment_method_id']}",
                                   callback_data=f"payment:{payment['payment_method_id']}"))
    return m
