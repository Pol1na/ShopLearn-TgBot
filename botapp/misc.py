from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.contrib.fsm_storage.redis import RedisStorage2

from asyncio import get_event_loop, Lock

from botapp.config import TOKEN


bot = Bot(TOKEN, parse_mode='HTML')
storage = MemoryStorage() #redis2
loop = get_event_loop()
dp = Dispatcher(bot, loop, storage)
lock = Lock()
