from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from botapp import markup
from botapp import config
from botapp.states import Admin
from botapp.misc import bot, dp


@dp.message_handler(lambda message: message.chat.id in config.admin_id,
                    commands=['admin'],
                    state='*')
async def process_admin(message: Message, state: FSMContext):
    await state.finish()
    await Admin.main.set()
    await bot.send_message(message.chat.id,
                           'Админ-меню',
                           reply_markup=markup.admin())
