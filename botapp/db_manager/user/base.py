from botapp.db_manager.connections import *


async def is_user(user_id):
    con, cur = await create_con()
    await cur.execute('select tg_user_id from user where tg_user_id = %s', (user_id,))
    user = await cur.fetchone()
    await con.ensure_closed()
    return user


async def reg_user(user_id):
    con, cur = await create_con()
    await cur.execute('insert into user '
                      '  (tg_user_id) '
                      'values '
                      '  (%s)',
                      (user_id,))
    await con.commit()
    await con.ensure_closed()


async def reg_cart(user_id):
    con, cur = await create_con()
    await cur.execute('select tg_user_id from user where tg_user_id = %s', (user_id,))
    bd_user_id = cur.fetchone()
    await cur.execute('insert into cart '
                      '(user_id)'
                      'values '
                      '(%s)',
                      (bd_user_id,))
    await con.commit()
    await con.ensure_closed()


async def get_user(user_id):
    con, cur = await create_dict_con()
    await cur.execute(f'select name, surname, patronymic, phone, address'
                      f' from user '
                      f'where (tg_user_id) = {str(user_id)}')
    user_data = await cur.fetchone()
    await con.ensure_closed()
    for index, item in enumerate(user_data):
        if user_data[item] is None:
            user_data[item] = 'Нет данных'
    print(user_data)
    if user_data['name'] and user_data['surname'] and user_data['patronymic'] == 'Нет данных':
        user_data.pop('surname')
        user_data.pop('patronymic')
    else:
        fiolist = user_data['name'], user_data['surname'], user_data['patronymic']
        fio = ' '.join(fiolist)
        user_data['name'] = fio
        user_data.pop('surname')
        user_data.pop('patronymic')
    return user_data


async def update_user_data(user_id, name=None, phone=None, address=None, user_data=None, is_all=False):
    con, cur = await create_con()
    if phone:
        await cur.execute("update user "
                          f"set phone = '{phone}' "
                          f"where tg_user_id = {str(user_id)} "
                          )

    elif name:
        name = name.split(' ')
        await cur.execute("update user "
                          f"set name = '{name[0]}', surname = '{name[1]}', patronymic = '{name[2]}' "
                          f"where tg_user_id = {str(user_id)}")

    elif address:
        await cur.execute("update user "
                          f"set address = '{address}' "
                          f"where tg_user_id = {str(user_id)} "
                          )

    elif is_all:
        print(user_data)
        name = user_data['name'].split(' ')
        sql = "update user " \
              f"set name = '{name[1]}', surname = '{name[0]}', patronymic = '{name[2]}', phone = '{user_data['phone']}', " \
              f"address = '{user_data['address']}' " \
              f"where (tg_user_id) = {str(user_id)}"
        print(sql)
        await cur.execute(sql)
        await con.commit()
        await con.ensure_closed()


async def get_helpers():
    con, cur = await create_dict_con()
    query = f"select (phone), (email)" \
            f"from helper"
    await cur.execute(query)
    helpers = await cur.fetchall()
    await con.ensure_closed()
    string = 'Контакты тех.поддержки \n\n'
    for helper in helpers:
        string += f"Номер телефона: {helper['phone']}\n" \
                  f"Email: {helper['email']}\n"
    return string
