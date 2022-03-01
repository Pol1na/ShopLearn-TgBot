from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from botapp import utils
from botapp import markup
from botapp.states import Admin
from botapp.misc import bot, dp


@dp.callback_query_handler(text_startswith='edit_product:', state=Admin.main)
async def edit_choice_product(call: CallbackQuery):
    product_id = call.data.split(':')[-1]
    await utils.edit_product_menu(user_id=call.message.chat.id,
                                  product_id=product_id,
                                  for_edit=call.message.message_id)


@dp.callback_query_handler(text_startswith='goproduct', state=Admin.main)
async def back_to_product(call: CallbackQuery):
    product_id = call.data.split(':')[-1]
    await utils.back_to_prod_cart(call, product_id)


@dp.callback_query_handler(text_startswith='product_edit:', state=Admin.main)
async def edit_product(call: CallbackQuery):
    choice = call.data.split(':')[1]
    Admin.EditProduct.product_id = call.data.split(':')[-1]
    if choice == 'name':
        await call.message.answer('Введите название продукта')
        await Admin.EditProduct.name.set()

    elif choice == 'desc':
        await call.message.answer('Введите описание продукта')
        await Admin.EditProduct.desc.set()

    elif choice == 'price':
        await call.message.answer('Введите цену продукта')
        await Admin.EditProduct.price.set()

    elif choice == 'photo':
        await call.message.answer('Отправьте фото продукта')
        await Admin.EditProduct.photo.set()


@dp.message_handler(state=Admin.EditProduct.name)
async def edit_name_product(message: Message, state: FSMContext):
    await state.finish()
    data = message.text
    await utils.edit_product(message.chat.id, data, Admin.EditProduct.product_id, 'name')


@dp.message_handler(state=Admin.EditProduct.desc)
async def edit_name_product(message: Message, state: FSMContext):
    await state.finish()
    data = message.text
    await utils.edit_product(message.chat.id, data, Admin.EditProduct.product_id, 'description')


@dp.message_handler(state=Admin.EditProduct.price)
async def edit_name_product(message: Message, state: FSMContext):
    await state.finish()
    data = message.text
    await utils.edit_product(message.chat.id, data, Admin.EditProduct.product_id, 'price')


@dp.message_handler(state=Admin.EditProduct.photo, content_types=[ContentType.PHOTO])
async def edit_name_product(message: Message, state: FSMContext):
    await state.finish()
    data = message.photo[-1].file_id
    await utils.edit_product(message.chat.id, data, Admin.EditProduct.product_id, 'photo')


@dp.callback_query_handler(text_startswith='delete_product', state=Admin.main)
async def delete_product(call: CallbackQuery):
    product_id = call.data.split(':')[-1]
    await utils.delete_prod(call.message.chat.id, product_id)
