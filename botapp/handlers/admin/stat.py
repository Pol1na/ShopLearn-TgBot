from aiogram.types import Message

from botapp import db_manager
from botapp.misc import bot, dp
from botapp.states import Admin


@dp.message_handler(text='Статистика', state=Admin.main)
async def process_bot_stata(message: Message):
    stat = await db_manager.get_bot_stat()
    await bot.send_message(message.chat.id,
                           'Человек в боте: {}'.format(stat.get('users_count')))
