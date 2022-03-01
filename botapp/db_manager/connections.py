from aiomysql import connect, Connection, Cursor, DictCursor
from pymysql import connect as sync_connect
from botapp.config import db


async def create_con():
    con: Connection = await connect(**db)
    cur: Cursor = await con.cursor()
    return con, cur


async def create_dict_con():
    con: Connection = await connect(**db)
    cur: DictCursor = await con.cursor(DictCursor)
    return con, cur


def sync_create_con():
    con = sync_connect(**db)
    cur = con.cursor()
    return con, cur
