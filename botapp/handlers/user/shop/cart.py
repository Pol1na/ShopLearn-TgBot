from aiogram.types import Message, CallbackQuery
from aiogram import exceptions
from botapp import utils
from botapp import markup
from botapp import db_manager
from botapp.states import User
from botapp.misc import bot, dp
from botapp import utils


@dp.message_handler(text='Корзина', state=User.main)
async def process_items(message: Message):
    await utils.show_user_cart(message)


@dp.callback_query_handler(text='clear-cart', state=User.main)
async def clear_user_cart(call: CallbackQuery):
    await utils.clear_cart(call)
