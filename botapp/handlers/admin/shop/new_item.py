from aiogram import exceptions
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from botapp import utils
from botapp import markup
from botapp.states import Admin
from botapp.misc import bot, dp


@dp.message_handler(text='Отменить', state=Admin.AddProduct)
async def cancel(message: Message, state: FSMContext):
    await message.answer('Добавление товара отменено', reply_markup=markup.admin())
    await state.finish()
    await Admin.main.set()


@dp.callback_query_handler(text_startswith='add_product', state=Admin.main)
async def add_prod_name(call: CallbackQuery):
    category_id = call.data.split(':')[-1]
    Admin.AddProduct.category_id = category_id
    await call.message.answer('Введите название товара',
                              reply_markup=markup.cancel())
    await Admin.AddProduct.name.set()


@dp.message_handler(state=Admin.AddProduct.name)
async def add_prod_desc(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание товара',
                         reply_markup=markup.cancel(skip=True))
    await Admin.AddProduct.desc.set()


@dp.message_handler(text='Пропустить', state=Admin.AddProduct.desc)
async def skip_desc(message: Message, state: FSMContext):
    await state.update_data(description='Описание отсутсвует')
    await message.answer('Отправьте фото товара',
                         reply_markup=markup.cancel(skip=True))
    await Admin.AddProduct.photo.set()


@dp.message_handler(state=Admin.AddProduct.desc)
async def add_prod_photo(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Отправьте фото товара',
                         reply_markup=markup.cancel(skip=True))
    await Admin.AddProduct.photo.set()


@dp.message_handler(text='Пропустить', state=Admin.AddProduct.photo)
async def skip_photo(message: Message, state: FSMContext):
    await state.update_data(photo='Фото отсутствует')
    await message.answer('Отправьте цену товара',
                         reply_markup=markup.cancel())
    await Admin.AddProduct.price.set()


@dp.message_handler(state=Admin.AddProduct.photo, content_types=[ContentType.PHOTO])
async def add_prod_price(message: Message, state: FSMContext):
    data = message.photo[-1].file_id
    await state.update_data(photo=data)
    await message.answer('Введите цену товара', reply_markup=markup.cancel())
    await Admin.AddProduct.price.set()


@dp.message_handler(state=Admin.AddProduct.price)
async def add_prod(message: Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        product_data = await state.get_data()
        product_data['category_id'] = Admin.AddProduct.category_id
        await state.finish()
        await utils.add_product(message.chat.id, product_data)

    except TypeError:
        await message.answer('Введите корректную цену товара')
        await Admin.AddProduct.price.set()
