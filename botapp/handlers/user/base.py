from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from botapp import markup
from botapp import db_manager
from botapp.states import User
from botapp.misc import bot, dp


@dp.message_handler(commands=['start'], state='*')
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    if not await db_manager.is_user(message.chat.id):
        await db_manager.reg_user(message.chat.id)
    await User.main.set()
    await bot.send_message(message.chat.id,
                           'Главное меню',
                           reply_markup=markup.main())
