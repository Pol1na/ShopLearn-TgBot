from botapp.db_manager.connections import *


async def get_bot_stat():
    con, cur = await create_dict_con()
    await cur.execute('select count(user_id) as users_count from user')
    users = await cur.fetchone()
    await con.ensure_closed()
    return users
