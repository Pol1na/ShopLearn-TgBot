from aiogram.types import Message, CallbackQuery

from botapp import utils
from botapp import markup
from botapp import db_manager
from botapp.states import User
from botapp.misc import bot, dp


@dp.message_handler(text='Мои данные', state=User.PersonalCab.main)
async def process_my_data(message: Message):
    user_data = await db_manager.get_user(message.chat.id)
    await bot.send_message(message.chat.id,
                           utils.user_data_message(user_data),
                           reply_markup=markup.edit_user_data())


