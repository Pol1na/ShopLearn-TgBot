from aiogram import exceptions
from aiogram.utils.exceptions import BadRequest
from . import *
from botapp import states
from botapp import db_manager
from botapp import markup
from botapp.misc import bot
from botapp.config import channel_id
from ..states import Admin


async def user_all_cats_message(user_id, what_need, parent_id=None, page=1, for_edit=None):
    categories, what_need = await db_manager.user_get_categories(what_need, parent_id)
    if for_edit:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=for_edit,
                                    text='Выберите интересующий Вас раздел',
                                    reply_markup=markup.user_categories(categories, what_need, page, parent_id))
    else:
        await bot.send_message(user_id,
                               'Выберите интересующий Вас раздел',
                               reply_markup=markup.user_categories(categories, what_need, page, parent_id))


async def show_product(product_id, call):
    data = await db_manager.get_product_data(product_id)
    data = data[0]
    photo = data['photo']
    try:
        await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo)
    except BadRequest:
        await call.message.answer('Фото отсутствует')
    await call.message.answer(f"{data['name']} \n \n Цена: {data['price']} UAH \n \n {data['description']}",
                              reply_markup=markup.gen_subaddtocart_menu(product_id))


async def add_to_cart(call):
    print(call.data)
    product_id = call.data.split(':')[-1]
    amount = call.data.split(':')[1]
    await db_manager.add_product_to_cart(product_id, call.message.chat.id, amount)
    await call.message.answer('Товар добавлен в корзину!')
    data = (await db_manager.get_product_data(product_id))[0]
    print(data)
    photo = data['photo']
    try:
        await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo)
    except BadRequest:
        await call.message.answer('Фото отсутствует')
    await call.message.answer(f"{data['name']} \n \n Цена: {data['price']} UAH \n \n {data['description']} \n \n"
                              f"В корзине: {amount}",
                              reply_markup=markup.gen_subaddtocart_menu(product_id))


async def show_user_cart(message):
    string = await db_manager.get_cart_data(message.chat.id)
    await message.answer(string, reply_markup=markup.user_cart())


async def clear_cart(call):
    await db_manager.clear_cart(call.message.chat.id)
    await call.message.answer('Корзина успешно очищена!', reply_markup=markup.main())


async def check_userdata(call):
    is_data, summa = await db_manager.check_user_data(call.message.chat.id)
    print(summa)
    if summa:
        if is_data:
            user_data = await db_manager.get_user(call.message.chat.id)
            msg = order_data_message(user_data)
            await call.message.answer(msg, reply_markup=markup.use_data())
        else:
            await call.message.answer('Пожалуйста, введите ФИО через пробел', reply_markup=markup.cancel())
            await states.User.Order.CreateData.name.set()
    else:
        await call.message.answer('Сумма корзины при формировании заказа не может быть равна нулю\n'
                                  'Пожалуйста, выберите что-нибудь', reply_markup=markup.main())


async def payment_data_message():
    payments_data = await db_manager.get_payments()
    msg_text = 'Выберите один из вариантов оплаты: \n\n'
    for payment in payments_data:
        msg_text += f"{payment['payment_method_id']}. {payment['name']}\n "
    menu = markup.payments(payments_data)
    return msg_text, menu


async def create_order(user_id, method, userdata=None):
    foradm, thanks = await db_manager.create_order_db(user_id, method, userdata)
    await bot.send_message(chat_id=channel_id,
                           text=foradm)
    await bot.send_message(chat_id=user_id,
                           text=thanks, reply_markup=markup.main())


async def categ_admin(user_id, what_need, parent_id=None, page=1, for_edit=None):
    categories, what_need = await db_manager.admin_get_categories(what_need, parent_id)
    if for_edit:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=for_edit,
                                    text='Ваш магазин',
                                    reply_markup=markup.admin_categories(categories, what_need, page, parent_id))
    else:
        await bot.send_message(user_id,
                               'Ваш магазин',
                               reply_markup=markup.admin_categories(categories, what_need, page, parent_id))


async def other_categ_admin(user_id, what_need, page=1, parent_id=None, for_edit=None):
    categories, result = await db_manager.admin_get_categories(what_need, parent_id)
    if for_edit:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=for_edit,
                                    text='Ваш магазин',
                                    reply_markup=markup.admin_other_categories(result, page, parent_id))
    else:
        await bot.send_message(user_id,
                               'Ваш магазин',
                               reply_markup=markup.admin_other_categories(result, page, parent_id))


async def get_products_menu(user_id, parent_id, page=1, for_edit=None):
    products, amount = await db_manager.get_products_in_category(parent_id)
    if for_edit:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=for_edit,
                                    text='Товары',
                                    reply_markup=markup.product_menu_cat(parent_id, amount, products, page))
    else:
        await bot.send_message(user_id,
                               'Товары',
                               reply_markup=markup.product_menu_cat(parent_id, amount, products, page))


async def get_product_data(call, product_id, category_id):
    data = await db_manager.get_product_data(product_id)
    data = data[0]
    photo = data['photo']
    try:
        await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo)
    except BadRequest:
        await call.message.answer('Фото отсутствует')
    await call.message.answer(f"{data['name']} \n \n Цена: {data['price']} UAH \n \n {data['description']}",
                              reply_markup=markup.edit_product(product_id, category_id))


async def back_to_prod_cart(call, product_id):
    category_id = await db_manager.get_category_id(product_id)
    await get_product_data(call, product_id, category_id)


async def edit_product_menu(user_id, product_id, for_edit=None):
    if for_edit:
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=for_edit,
                                    text='Товары',
                                    reply_markup=markup.choice_to_edit(product_id))
    else:
        await bot.send_message(user_id,
                               'Товары',
                               reply_markup=markup.choice_to_edit(product_id))


async def edit_product(user_id, data, product_id, what_need):
    await db_manager.change_product_data(product_id, data, what_need)
    await Admin.main.set()
    await bot.send_message(chat_id=user_id,
                           text='Данные обновлены',
                           reply_markup=await categ_admin(user_id, 'category'))


async def delete_prod(user_id, product_id):
    await db_manager.delete_product(product_id)
    await Admin.main.set()
    await bot.send_message(chat_id=user_id,
                           text='Товар успешно удален',
                           reply_markup=await categ_admin(user_id, 'category'))


async def add_product(user_id, product_data):
    await db_manager.add_prod(product_data)
    await Admin.main.set()
    await bot.send_message(chat_id=user_id,
                           text='Товар успешно добавлен',
                           reply_markup=markup.admin())


async def add_subcat(user_id, name, parent_id):
    await db_manager.add_subcategory(name, parent_id)
    await Admin.main.set()
    await bot.send_message(chat_id=user_id,
                           text='Категория добавлена',
                           reply_markup=await categ_admin(user_id, 'category'))


async def del_category(user_id, parent_id):
    await db_manager.delete_category(parent_id)
    await Admin.main.set()
    await bot.send_message(chat_id=user_id,
                           text='Категория удалена',
                           reply_markup=await categ_admin(user_id, 'category'))
