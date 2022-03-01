import math

from botapp.db_manager.connections import *


async def admin_get_categories(what_need, parent_id=None):
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
    if not data:
        sql = f"select product_id, category_id, name " \
              f"from product " \
              f"where category_id = {int(parent_id)}"
        await cur.execute(sql)
        data = await cur.fetchall()
        if data:
            await con.ensure_closed()
            return data, 'product_category'
        await con.ensure_closed()
        return data, 'empty_category'
    else:
        await con.ensure_closed()
        return data, 'category_subcategories'


async def get_products_in_category(parent_id):
    con, cur = await create_dict_con()
    sql = f"select product_id, category_id, name " \
          f"from product " \
          f"where category_id = {int(parent_id)}"
    await cur.execute(sql)
    data = await cur.fetchall()
    amount = math.ceil(len(data) / 8)
    await con.ensure_closed()
    return data, amount


async def change_product_data(product_id, data, what_need):
    con, cur = await create_dict_con()
    sql = 'update product ' \
          f"set {what_need} = '{data}' " \
          f"where product_id = {product_id}"
    await cur.execute(sql)
    await con.commit()
    await con.ensure_closed()


async def delete_product(product_id):
    con, cur = await create_dict_con()
    sql = 'delete from product ' \
          f'where product_id = {product_id}'
    await cur.execute(sql)
    await con.commit()
    await con.ensure_closed()


async def add_prod(product_data):
    con, cur = await create_dict_con()
    sql = 'insert into product ' \
          '(category_id, name, price, description, photo) ' \
          'values ' \
          f"({product_data['category_id']}, '{product_data['name']}', {product_data['price']}," \
          f" '{product_data['description']}', '{product_data['photo']}')"
    await cur.execute(sql)
    await con.commit()
    await con.ensure_closed()

async def get_category_id(product_id):
    con, cur = await create_con()
    sql = 'select category_id ' \
          'from product ' \
          f'where product_id = {product_id}'
    await cur.execute(sql)
    category_id = await cur.fetchone()
    return category_id

async def add_subcategory(name, parent_id):
    con, cur = await create_dict_con()
    sql = 'insert into category ' \
          '(name, parent_category_id) ' \
          'values ' \
          f"('{name}', {parent_id})"
    await cur.execute(sql)
    await con.commit()
    await con.ensure_closed()


async def delete_category(category_id):
    con, cur = await create_dict_con()
    sql = 'delete from product ' \
          f'where category_id = {category_id}'
    await cur.execute(sql)
    await con.commit()
    sql = 'delete from category ' \
          f'where parent_category_id = {category_id}'
    await cur.execute(sql)
    await con.commit()
    sql = 'delete from category ' \
          f'where category_id = {category_id}'
    await cur.execute(sql)
    await con.commit()
    await con.ensure_closed()
