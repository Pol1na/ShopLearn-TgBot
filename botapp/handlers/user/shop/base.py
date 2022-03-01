from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import exceptions
from botapp import utils
from botapp import markup
from botapp import db_manager
from botapp.states import User
from botapp.misc import bot, dp
from botapp import utils


@dp.message_handler(text='Магазин', state=User.main)
async def process_items(message: Message):
    await utils.user_all_cats_message(message.chat.id, what_need='category')


@dp.callback_query_handler(text='back_btn', state=User.main)
async def back(call:CallbackQuery):
    await utils.user_all_cats_message(call.message.chat.id, what_need='category')


@dp.callback_query_handler(text_startswith="pagination:", state=User.main)
async def pagination_categories(call: CallbackQuery):
    what_need, parent_id, page = call.data.split(':')[1], call.data.split(':')[2], call.data.split(':')[3]
    await utils.user_all_cats_message(call.message.chat.id,
                                      what_need=what_need,
                                      parent_id=parent_id,
                                      page=page,
                                      for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith="shop_menu:showproduct", state=User.main)
async def show_product_data(call: CallbackQuery):
    product_id = call.data.split(':')[2]
    await utils.show_product(product_id, call)


@dp.callback_query_handler(text_startswith="shop_menu:", state=User.main)
async def pagination_subcategories(call: CallbackQuery):
    category_id = call.data.split(':')[2]
    what_need = call.data.split(':')[1]
    await utils.user_all_cats_message(call.message.chat.id,
                                      what_need=what_need,
                                      parent_id=category_id,
                                      for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith="back-to-category", state=User.main)
async def back_to_categories(call: CallbackQuery):
    await utils.user_all_cats_message(call.message.chat.id, what_need='category', for_edit=call.message.message_id)


# вручную????
@dp.callback_query_handler(text_startswith='subadd_cart:', state=User.main)
async def add_to_cart(call: CallbackQuery):
    print(call.data)
    product_id = call.data.split(':')[-1]
    await call.message.answer('Выберите количество для добавления в корзину \n (Вы можете ввести значения вручную)',
                              reply_markup=markup.gen_add_to_cart(product_id))


@dp.callback_query_handler(text_startswith='amount', state=User.main)
async def amount(call: CallbackQuery):
    product_id = call.data.split(':')[-1]
    number = call.data.split(':')[1]
    if 'minus' in call.data:
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text=' Выберите количество для добавления в корзину \n (Вы можете ввести значения вручную)',
                                         reply_markup=markup.gen_add_to_cart(product_id, int(number) - 1))
    elif 'plus' in call.data:
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text=' Выберите количество для добавления в корзину \n (Вы можете ввести значения вручную)',
                                         reply_markup=markup.gen_add_to_cart(product_id, int(number) + 1))


@dp.callback_query_handler(text_startswith='add_cart:', state=User.main)
async def add_cart_func(call: CallbackQuery):
    await utils.add_to_cart(call)
