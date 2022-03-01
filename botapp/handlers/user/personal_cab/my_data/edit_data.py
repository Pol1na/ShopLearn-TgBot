from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

from botapp import markup
from botapp import db_manager
from botapp.states import User
from botapp.misc import bot, dp
from .base import process_my_data



@dp.message_handler(text='Отменить', state=User.PersonalCab.EditData)
async def cancel_edit_userdata(message: Message):
    await User.PersonalCab.main.set()
    await message.answer(text='Редактирование данных отменено',
                         reply_markup=markup.personal_cab_menu())


@dp.callback_query_handler(text_startswith='edit-my-data', state=User.PersonalCab.main)
async def edit_my_data(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Выберите, что Вы хотите редактировать',
                                reply_markup=markup.edit_user_data(edit=True))


@dp.callback_query_handler(text_startswith='edit-user-data:', state='*')
async def edit_user_data(call: CallbackQuery):
    await call.answer()
    what = call.data.split(':')[-1]
    if what == 'phone':
        await call.message.delete()
        await call.message.answer('Пожалуйста, отправьте Ваш контактный номер телефона воспользовавшись кнопкой ниже, ',
                                  reply_markup=markup.cancel(request_contact=True))
        await User.PersonalCab.EditData.phone.set()
    elif what == 'fio':
        await call.message.delete()
        await User.PersonalCab.EditData.name.set()
        await call.message.answer('Введите ФИО',
                                  reply_markup=markup.cancel())
    elif what == 'address':
        await call.message.delete()
        await User.PersonalCab.EditData.address.set()
        await call.message.answer('Укажите новый адрес доставки',
                                  reply_markup=markup.cancel())


@dp.message_handler(state=User.PersonalCab.EditData.phone, content_types=['contact'])
async def edit_data_phone(message: Message):
    phone = message['contact']['phone_number']
    await db_manager.update_user_data(message.chat.id, phone=phone)
    await User.PersonalCab.main.set()
    await message.answer('Изменения сохранены',
                         reply_markup=markup.personal_cab_menu())
    await process_my_data(message)


@dp.message_handler(state=User.PersonalCab.EditData.name)
async def edit_data_name(message: Message):
    name = message.text
    if len(name.split(' ')) == 3:
        await db_manager.update_user_data(message.chat.id, name=name)
        await User.PersonalCab.main.set()
        await message.answer('Изменения сохранены',
                             reply_markup=markup.personal_cab_menu())
    else:
        await message.answer('Введите корректное ФИО')


@dp.message_handler(state=User.PersonalCab.EditData.address)
async def edit_data_address(message: Message):
    address = message.text
    await db_manager.update_user_data(message.chat.id, address=address)
    await User.PersonalCab.main.set()
    await message.answer('Изменения сохранены',
                         reply_markup=markup.personal_cab_menu())
