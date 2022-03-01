from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import exceptions
from botapp import utils, db_manager
from botapp import markup
from botapp.states import User
from botapp.misc import bot, dp
from botapp import utils
from botapp.utils import messages


@dp.message_handler(text='Отменить', state=User.Order.CreateData)
async def cancel_data(message: Message):
    await User.main.set()
    await message.answer('Обновление данных отменено', reply_markup=markup.main())


@dp.message_handler(text='Пропустить', state=User.Order.CreateData.address)
async def skip_data(message: Message, state: FSMContext):
    await state.update_data(address='Не указан')
    await message.answer('Отправьте ваш номер телефона, чтобы менеджер мог связаться с вами в случае необходимости',
                         reply_markup=markup.cancel(request_contact=True))
    await User.Order.CreateData.phone.set()


@dp.callback_query_handler(text_startswith='form-order', state=User.main)
async def form_order(call: CallbackQuery):
    await utils.check_userdata(call)


@dp.callback_query_handler(text_startswith='use_this_data', state=User.main)
async def using_data(call: CallbackQuery):
    choice = call.data.split(':')[-1]
    if choice == 'yes':
        msg, menu = await utils.payment_data_message()
        await call.message.answer(msg, reply_markup=menu)
        await User.Order.CreateData.accept.set()
    else:
        await call.message.answer('Введите ФИО')
        await User.Order.CreateData.name.set()


@dp.message_handler(state=User.Order.CreateData.name)
async def order_name(message: Message, state: FSMContext):
    print(message.text)
    if len(message.text.split(' ')) == 3:
        await state.update_data(name=message.text)
        await message.answer('Введите адрес доставки:',
                             reply_markup=markup.cancel(skip=True))
        await User.Order.CreateData.address.set()
    else:
        await message.answer('Введите корректное ФИО',
                             reply_markup=markup.cancel())
        await User.Order.CreateData.name.set()


@dp.message_handler(state=User.Order.CreateData.address)
async def order_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Отправьте ваш номер телефона, чтобы менеджер мог связаться с вами в случае необходимости',
                         reply_markup=markup.cancel(request_contact=True))
    await User.Order.CreateData.phone.set()


@dp.message_handler(state=User.Order.CreateData.phone, content_types=['contact'])
async def order_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message['contact']['phone_number'])
    user_data = await state.get_data()
    print(user_data)
    await message.answer(utils.order_newdata_message(user_data),
                         reply_markup=markup.check_save_data())


@dp.callback_query_handler(text_startswith='save-new-order-data:', state=User.Order)
async def saving_user_data(call: CallbackQuery, state: FSMContext):
    is_saving = call.data.split(':')[-1]
    user_data = await state.get_data()
    if is_saving == 'yes':
        await db_manager.update_user_data(call.message.chat.id, user_data=user_data, is_all=True)
        msg, menu = await utils.payment_data_message()
        await call.message.answer(msg, reply_markup=menu)
        await User.Order.CreateData.accept.set()
    else:
        msg, menu = await utils.payment_data_message()
        await call.message.answer(msg, reply_markup=menu)
        await User.Order.CreateData.decline.set()


@dp.callback_query_handler(text_startswith='payment:', state=User.Order.CreateData.decline)
async def not_save_data(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await state.finish()
    await User.main.set()
    payment_method = call.data.split(':')[-1]
    await utils.create_order(call.message.chat.id, payment_method, user_data)


@dp.callback_query_handler(text_startswith='payment:', state=User.Order.CreateData.accept)
async def yes_save_data(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await User.main.set()
    payment_method = call.data.split(':')[-1]
    await utils.create_order(call.message.chat.id, payment_method)
