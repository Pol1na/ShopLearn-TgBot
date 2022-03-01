from aiogram.types import Message

from botapp import db_manager
from botapp.states import User
from botapp.misc import bot, dp


@dp.message_handler(text='Помощь', state=User.main)
async def process_help(message: Message):
    await message.answer(await db_manager.get_helpers())
