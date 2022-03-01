from aiogram.types import \
    InlineKeyboardMarkup, \
    InlineKeyboardButton, \
    KeyboardButton, \
    ReplyKeyboardMarkup



def admin_categories(categories_data, what_need, page=1, parent_id=None):
    m = InlineKeyboardMarkup(resize_keyboard=True)
    item_on_page = 8
    add_new_category = InlineKeyboardButton(text='Добавить категорию', callback_data='add_new_maincategory')
    if len(categories_data) != 0:
        for category in categories_data[(int(page) * item_on_page) - item_on_page:int(page) * item_on_page]:
            m.row(InlineKeyboardButton(text=category['name'],
                                       callback_data=f"shop_menu:{what_need}:{category['category_id']}"))
        m.row(add_new_category)

    else:
        m.row(add_new_category)
    if parent_id != 'None' and parent_id is not None:
        m.row(InlineKeyboardButton(text='Назад', callback_data=f'mainback-btn:{parent_id}'))

    m.row(InlineKeyboardButton(text='<', callback_data=f"pagination:{parent_id}:{int(page) - 1}"),
          InlineKeyboardButton(text='>', callback_data=f"pagination:{parent_id}:{int(page) + 1}"))

    return m


def admin_other_categories(result, page=1, parent_id=None):
    if page < 1:
        page = 1
    m = InlineKeyboardMarkup(resize_keyboard=True)
    print(parent_id)
    subcategories = InlineKeyboardButton(text='Подкатегории', callback_data=f'category-get:{page}:{parent_id}')
    delete_category = InlineKeyboardButton(text='Удалить категорию', callback_data=f'delete-category:{parent_id}')
    add_new_category = InlineKeyboardButton(text='Добавить категорию', callback_data=f'add_new_subcategory:{parent_id}')
    add_new_product = InlineKeyboardButton(text='Добавить товар', callback_data=f'add_product:{parent_id}')
    back_btn = InlineKeyboardButton(text='Назад', callback_data=f'mainback-btn:{parent_id}')
    products = InlineKeyboardButton(text='Товары', callback_data=f'get-products:{page}:{parent_id}')
    if result == 'empty_category':
        m.add(add_new_product)
        m.add(add_new_category)
        m.add(back_btn)
    if result == 'category_subcategories':
        m.add(subcategories)
        m.add(delete_category)
        m.add(back_btn)
    if result == 'product_category':
        m.add(products)
        m.add(delete_category)
        m.add(back_btn)

    return m


def product_menu_cat(parent_id, amount, products, page=1):
    if page < 1:
        page = 1
    m = InlineKeyboardMarkup(resize_keyboard=True)
    item_on_page = 8

    add_product = InlineKeyboardButton(text='Добавить товар', callback_data=f'add_product:{parent_id}')
    next_page_btn = InlineKeyboardButton(text='<', callback_data=f'product_page:{int(page) - 1}:{parent_id}')
    amount_btn = InlineKeyboardButton(text=f'{page}/{amount}', callback_data=f'amount')
    b_page_btn = InlineKeyboardButton(text='>', callback_data=f'product_page:{int(page) + 1}:{parent_id}')

    for product in products[(int(page) * item_on_page) - item_on_page:int(page) * item_on_page]:
        m.add(InlineKeyboardButton(text=f"{str(product['name'])}",
                                   callback_data=f"showproduct:{product['product_id']}:{parent_id}"))
    m.add(next_page_btn, amount_btn, b_page_btn)
    m.add(add_product)
    return m


def edit_product(product_id, category_id):
    m = InlineKeyboardMarkup(resize_keyboard=True)
    edit_btn = InlineKeyboardButton(text='Редактировать товар', callback_data=f'edit_product:{product_id}')
    delete_btn = InlineKeyboardButton(text='Удалить товар', callback_data=f'delete_product:{product_id}')
    back_btn = InlineKeyboardButton(text='К товарам', callback_data=f'to_products:1:{category_id}')
    m.add(edit_btn)
    m.add(delete_btn)
    m.add(back_btn)
    return m

def choice_to_edit(product_id):
    m = InlineKeyboardMarkup(resize_keyboard=True)
    name = InlineKeyboardButton(text='Название', callback_data=f'product_edit:name:{product_id}')
    description = InlineKeyboardButton(text='Описание', callback_data=f'product_edit:desc:{product_id}')
    price = InlineKeyboardButton(text='Цена', callback_data=f'product_edit:price:{product_id}')
    photo = InlineKeyboardButton(text='Фото', callback_data=f'product_edit:photo:{product_id}')
    back_btn = InlineKeyboardButton(text='Назад', callback_data=f'goproduct:{product_id}')
    m.row(name, description)
    m.row(price, photo)
    m.row(back_btn)
    return m