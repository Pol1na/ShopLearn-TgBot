from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram import executor
from botapp.misc import dp, bot

from aiohttp import web

# async def on_startup(dispatch):
#     web_hook = await bot.get_webhook_info()
#     if web_hook.url != WEBHOOK_URL:
#         if not web_hook.url:
#             await bot.delete_webhook()
#         await bot.set_webhook(WEBHOOK_URL, certificate=open('/etc/nginx/ssl/nginx.crt', 'r'))
#     # await bot.delete_webhook()
#     print(await bot.get_webhook_info())
#
#
# async def on_shutdown(dispatch):
#     await bot.delete_webhook()
#     await bot.close()
#     await dp.storage.close()
#     await dp.storage.wait_closed()
#

if __name__ == '__main__':

    from botapp.handlers import *

    # WEBHOOK_URL = 'https://185.86.76.211/megagen/'
    # app = get_new_configured_app(dispatcher=dp, path='/megagen/')
    # app.on_startup.append(on_startup)
    # app.on_shutdown.append(on_shutdown)
    # web.run_app(app, host='127.0.0.1', port=5151)
    executor.start_polling(dp, skip_updates=True)
