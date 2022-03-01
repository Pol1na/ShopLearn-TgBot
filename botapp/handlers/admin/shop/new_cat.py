from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from botapp import markup
from botapp import utils
from botapp.states import Admin
from botapp.misc import bot, dp


@dp.message_handler(text='Отменить', state=Admin.AddCategory)
async def cancel(message: Message, state:FSMContext):
    await state.finish()
    await Admin.main.set()
    await message.answer('Добавление категории отменено',
                         reply_markup=markup.admin())


@dp.message_handler(text='Отменить', state=Admin.AddMainCategory)
async def cancel(message: Message, state:FSMContext):
    await state.finish()
    await Admin.main.set()
    await message.answer('Добавление категории отменено',
                         reply_markup=markup.admin())


@dp.callback_query_handler(text_startswith='add_new_subcategory:', state=Admin.main)
async def add_subcat(call: CallbackQuery):
    parent_id = call.data.split(':')[-1]
    Admin.AddCategory.parent_id = parent_id
    await call.message.answer('Введите название новой категории',
                              reply_markup=markup.cancel())
    await Admin.AddCategory.name.set()


@dp.message_handler(state=Admin.AddCategory.name)
async def add_subcat_name(message: Message, state: FSMContext):
    await state.finish()
    await utils.add_subcat(message.chat.id, message.text, Admin.AddCategory.parent_id)


@dp.callback_query_handler(text_startswith='add_new_maincategory', state=Admin.main)
async def add_cat(call: CallbackQuery):
    await call.message.answer('Введите название новой категории',
                              reply_markup=markup.cancel())
    await Admin.AddMainCategory.name.set()


@dp.message_handler(state=Admin.AddMainCategory.name)
async def add_cat_name(message: Message, state: FSMContext):
    await state.finish()
    await utils.add_subcat(message.chat.id, message.text, 'null')


@dp.callback_query_handler(text_startswith='delete-category', state=Admin.main)
async def delete_category(call: CallbackQuery):
    parent_id = call.data.split(':')[-1]
    await utils.del_category(call.message.chat.id, parent_id)
