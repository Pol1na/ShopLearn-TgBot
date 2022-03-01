from aiogram.types import Message

from botapp import markup
from botapp.states import User
from botapp.misc import bot, dp


@dp.message_handler(text='Кабинет', state=User.main)
async def process_personal_cab(message: Message):
    await User.PersonalCab.main.set()
    await bot.send_message(message.chat.id,
                           'Личный кабинет',
                           reply_markup=markup.personal_cab_menu())


@dp.message_handler(text='В главное меню', state=User.PersonalCab.main)
async def back_to_main(message: Message):
    await User.main.set()
    await bot.send_message(message.chat.id,
                           'Главное меню',
                           reply_markup=markup.main())
