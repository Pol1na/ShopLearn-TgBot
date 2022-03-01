from aiogram import exceptions
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from botapp import utils
from botapp import markup
from botapp import db_manager
from botapp.states import Admin
from botapp.misc import bot, dp


@dp.message_handler(text='Магазин', state=Admin.main)
async def process_shop(message: Message, state: FSMContext):
    await state.finish()
    await Admin.main.set()
    await bot.send_message(message.chat.id,
                           'Меню магазина',
                           reply_markup=markup.admin())
    await utils.categ_admin(message.chat.id, what_need='category')



@dp.callback_query_handler(text_startswith='mainback-btn', state=Admin.main)
async def back_categ(call:CallbackQuery):
    await bot.send_message(call.message.chat.id,
                           'Меню магазина',
                           reply_markup=markup.admin())
    await utils.categ_admin(call.message.chat.id, what_need='category')


@dp.message_handler(text='Все категории', state=Admin.main)
async def get_all_cats(message: Message, state: FSMContext):
    await state.finish()
    await Admin.main.set()
    await utils.categ_admin(message.chat.id, what_need='category')


@dp.callback_query_handler(text_startswith="pagination:", state=Admin.main)
async def pagination_categories(call: CallbackQuery):
    print(call.data)
    parent_id, page = call.data.split(':')[1], call.data.split(':')[2]
    await utils.categ_admin(call.message.chat.id,
                            what_need='category',
                            parent_id=parent_id,
                            page=page,
                            for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith='shop_menu:', state=Admin.main)
async def get_other_categories(call: CallbackQuery):
    category_id = call.data.split(':')[-1]
    await utils.other_categ_admin(user_id=call.message.chat.id,
                                  what_need='category',
                                  parent_id=category_id,
                                  for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith='category-get:', state=Admin.main)
async def get_sub_categories(call: CallbackQuery):
    page, parent_id = call.data.split(':')[1], call.data.split(':')[-1]
    await utils.categ_admin(user_id=call.message.chat.id,
                            what_need='category',
                            page=page,
                            parent_id=parent_id,
                            for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith='get-products', state=Admin.main)
async def get_products_in_cat(call: CallbackQuery):
    category_id = call.data.split(':')[-1]
    await utils.get_products_menu(call.message.chat.id,
                                  category_id,
                                  for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith='product_page:', state=Admin.main)
async def pagination_products(call: CallbackQuery):
    page, parent_id = call.data.split(':')[1], call.data.split(':')[-1]
    await utils.get_products_menu(user_id=call.message.chat.id,
                                  parent_id=parent_id,
                                  page=page,
                                  for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith='showproduct:', state=Admin.main)
async def show_product(call: CallbackQuery):
    product_id, parent_id = call.data.split(':')[1], call.data.split(':')[-1]
    await utils.get_product_data(call, product_id, parent_id)


@dp.callback_query_handler(text_startswith='to_products:', state=Admin.main)
async def to_products(call: CallbackQuery):
    page, parent_id = call.data.split(':')[1], call.data.split(':')[-1]
    await utils.get_products_menu(user_id=call.message.chat.id,
                                  parent_id=parent_id,
                                  page=page,
                                  for_edit=call.message.message_id)

