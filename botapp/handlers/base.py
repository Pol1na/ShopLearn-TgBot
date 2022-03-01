from aiogram import exceptions
from botapp.misc import dp


@dp.errors_handler(exception=exceptions.InvalidQueryID)
async def invalid_query_id(update, error):
    return True


@dp.errors_handler(exception=exceptions.MessageToDeleteNotFound)
async def message_to_delete_not_found(update, error):
    return True


@dp.errors_handler(exception=exceptions.MessageCantBeDeleted)
async def message_cant_be_deleted(update, error):
    return True


# @dp.errors_handler(exception=exceptions.BadRequest)
# async def bad_request(update, error):
#     return True
