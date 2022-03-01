from botapp.db_manager.connections import *


async def user_get_categories(what_need, parent_id=None):
    con, cur = await create_dict_con()
    data = []
    if what_need == 'category':
        if parent_id is None or parent_id == 'None':
            query = f"select category_id, name " \
                    f"from category " \
                    f"where parent_category_id is Null"
        else:
            query = f"select category_id, name " \
                    f"from category " \
                    f"where parent_category_id = {parent_id}"
        await cur.execute(query)
        data = await cur.fetchall()
    if not data or what_need == 'get_products':
        sql = f"select product_id, category_id, name " \
              f"from product " \
              f"where category_id = {int(parent_id)}"
        await cur.execute(sql)
        data = await cur.fetchall()
        what_need = 'showproduct'
    await con.ensure_closed()
    return data, what_need


async def get_product_data(product_id):
    con, cur = await create_dict_con()
    query = f"select name, price, description, photo " \
            f"from product " \
            f"where product_id = {int(product_id)}"
    await cur.execute(query)
    product_data = await cur.fetchall()
    await con.ensure_closed()
    return product_data


async def add_product_to_cart(product_id, user_id, amount=1):
    con, cur = await create_con()
    full_price = 0
    full_amount = 0
    sql = "select user_id " \
          "from user " \
          f"where tg_user_id = {user_id}"
    await cur.execute(sql)
    bd_user_id = (await cur.fetchone())[0]
    sql = "select cart_id " \
          "from cart " \
          f"where user_id = {bd_user_id}"
    await cur.execute(sql)
    cart_id = (await cur.fetchone())[0]

    sql = "select price " \
          "from product " \
          f"where product_id = {product_id}"
    await cur.execute(sql)
    product_price = int((await cur.fetchone())[0])
    await con.ensure_closed()

    con, cur = await create_dict_con()
    sql = "select * " \
          "from product_in_cart " \
          f"where cart_id={cart_id} and product_id = {product_id}"
    await cur.execute(sql)

    if await cur.fetchone() != None:
        await cur.execute("select amount "
                          "from product_in_cart "
                          f"where product_id = {product_id} and cart_id = {cart_id}")
        curr_cart = (await cur.fetchall())[0]
        amount = int(amount) + int(curr_cart['amount'])
        sql = "update product_in_cart " \
              f"set price = {int(product_price) * int(amount)}, amount = {amount} " \
              f"where cart_id = {cart_id} and product_id = {product_id}"
        await cur.execute(sql)
        await con.commit()
    else:
        sql = "insert into product_in_cart(" \
              "cart_id, product_id, amount, price) " \
              "values(" \
              f"{cart_id}, {product_id}, {amount}, {int(amount) * int(product_price)})"
        await cur.execute(sql)
        await con.commit()

    await cur.execute('select price, amount '
                      'from product_in_cart '
                      f'where cart_id = {cart_id}')
    products_in_cart = await cur.fetchall()
    for item in products_in_cart:
        full_price += int(item['price'])
        full_amount += int(item['amount'])

    await cur.execute('update cart '
                      f'set amount = {full_amount}, summa = {full_price} '
                      f'where cart_id = {cart_id}')
    await con.commit()
    await con.ensure_closed()


async def get_cart_data(user_id):
    all_products = []
    con, cur = await create_dict_con()
    sql = "select user_id " \
          "from user " \
          f"where tg_user_id = {user_id}"
    await cur.execute(sql)
    bd_user_id = (await cur.fetchone())['user_id']
    sql = "select cart_id " \
          "from cart " \
          f"where user_id = {bd_user_id}"
    await cur.execute(sql)
    cart_id = (await cur.fetchone())['cart_id']

    sql = "select summa, amount " \
          "from cart " \
          f"where cart_id = {cart_id}"
    await cur.execute(sql)
    cart_data = await cur.fetchone()
    sql = "select product_id, amount, price " \
          "from product_in_cart " \
          f"where cart_id = {cart_id}"

    await cur.execute(sql)
    products_in_cart = await cur.fetchall()
    for product in products_in_cart:
        sql = "select name, price " \
              "from product " \
              f"where product_id = {product['product_id']}"
        await cur.execute(sql)
        all_products.append(await cur.fetchone())
    string = 'Моя корзина: \n'
    for i in range(0, len(all_products)):
        string += f"\n {all_products[i]['name']} | {products_in_cart[i]['amount']} x {all_products[i]['price']}\n"
    if cart_data['amount'] is None:
        cart_data['amount'] = 0
    if cart_data['summa'] is None:
        cart_data['summa'] = 0
    string += f"\n\n Итого: {cart_data['amount']} товаров на сумму {cart_data['summa']} UAH"

    return string


async def clear_cart(user_id):
    con, cur = await create_dict_con()
    sql = "select user_id " \
          "from user " \
          f"where tg_user_id = {user_id}"
    await cur.execute(sql)
    bd_user_id = (await cur.fetchone())['user_id']
    sql = "select cart_id " \
          "from cart " \
          f"where user_id = {bd_user_id}"
    await cur.execute(sql)
    cart_id = (await cur.fetchone())['cart_id']

    await cur.execute('delete from product_in_cart '
                      f'where cart_id = {cart_id}')
    await cur.execute('update cart '
                      'set amount = 0, summa = 0 '
                      f'where cart_id = {cart_id}')
    await con.commit()
    await con.ensure_closed()

