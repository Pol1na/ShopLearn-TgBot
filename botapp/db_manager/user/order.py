from datetime import datetime

from botapp.db_manager.connections import *


async def check_user_data(user_id):
    con, cur = await create_dict_con()
    sql = 'select name, surname, patronymic, phone, address ' \
          'from user ' \
          f'where tg_user_id = {user_id}'
    await cur.execute(sql)
    user_data = await cur.fetchone()
    sql = 'select cart.summa from cart ' \
          'inner join user on ' \
          'user.user_id = cart.user_id ' \
          f'where user.tg_user_id = {user_id}'
    await cur.execute(sql)
    cart = await cur.fetchone()
    if cart['summa'] == '0':
        summa = False
    else:
        summa = True
    for data in user_data.values():
        if data is None:
            return False, summa
    return True, summa


async def get_payments():
    con, cur = await create_dict_con()
    sql = 'select payment_method_id, name from payment_method'
    await cur.execute(sql)
    payment_data = await cur.fetchall()
    return payment_data


async def create_order_db(user_id, payment, userdata=None):
    con, cur = await create_dict_con()
    full_products = []
    await cur.execute(f'select user_id from user where tg_user_id = {user_id}')
    bd_user_id = (await cur.fetchone())['user_id']
    sql = "select cart_id, summa " \
          "from cart " \
          f"where user_id = {bd_user_id}"
    await cur.execute(sql)
    cart = await cur.fetchone()
    # if cart['summa'] == 0:
    sql = 'insert into ' \
          'orders(user_id,payment_id,cart_id,status,summa,created_at) ' \
          'values ' \
          f"({bd_user_id}, {payment}, {cart['cart_id']}, 'Отправлен на обработку', {cart['summa']}, '{datetime.date(datetime.now())}')"
    await cur.execute(sql)
    await con.commit()
    await cur.execute("select last_insert_id() from orders")
    order_id = (await cur.fetchone())['last_insert_id()']
    sql = 'select tg_name, name, surname, patronymic, phone, address ' \
          'from user inner join orders on orders.user_id = user.user_id ' \
          f'where orders.order_id = {order_id}'
    await cur.execute(sql)
    user_data = await cur.fetchone()
    sql = 'select payment_method.name from payment_method ' \
          'inner join orders ON ' \
          'orders.payment_id = payment_method.payment_method_id ' \
          f'where orders.order_id = {order_id}'
    await cur.execute(sql)
    payment_method = await cur.fetchone()
    sql = 'select amount, product_id ' \
          'from product_in_cart ' \
          f"where cart_id = {cart['cart_id']}"
    await cur.execute(sql)
    products_in_cart = await cur.fetchall()
    for product in products_in_cart:
        sql = 'select name, price ' \
              'from product ' \
              f"where product_id = {product['product_id']}"
        await cur.execute(sql)
        full_products.append(await cur.fetchone())
    string = ''
    for index in range(0, len(full_products)):
        string += f"\n {full_products[index]['name']} | {products_in_cart[index]['amount']} x {full_products[index]['price']}\n"
    if userdata:
        foradm = f"Пользователь @{user_data['tg_name']} | {userdata['name']} оформил заказ № {order_id}\n\n" \
                 f"Номер телефона: {userdata['phone']}\n" \
                 f"Адрес: {userdata['address']}\n" \
                 f"Способ оплаты: {payment_method['name']}\n" \
                 f"Сумма: {cart['summa']}\n" \
                 f"Товары: {string}\n"
    else:
        foradm = f"Пользователь @{user_data['tg_name']} | {user_data['name']} {user_data['surname']} {user_data['patronymic']} оформил заказ № {order_id}\n\n" \
                 f"Номер телефона: {user_data['phone']}\n" \
                 f"Адрес: {user_data['address']}\n" \
                 f"Способ оплаты: {payment_method['name']}\n" \
                 f"Сумма: {cart['summa']}\n" \
                 f"Товары: {string}\n"
    thanks = f"Спасибо, ваш заказ №{order_id} оформлен! \n\n" \
             f"Сумма итого: {cart['summa']} \n\n" \
             f"Вы получите уведомление о статусе заказа в боте!"
    return foradm, thanks
