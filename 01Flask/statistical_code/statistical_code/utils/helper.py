from settings import Config
import pymysql


def connect(c_type):  # 打开链接
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=c_type)  # 输出字典
    return conn, cursor


def connect_close(conn, cursor):  # 关闭连接
    cursor.close()
    conn.close()


def fetch_all(sql, args=None, c_type=pymysql.cursors.DictCursor):
    """查询所有记录"""
    conn, cursor = connect(c_type)

    cursor.execute(sql, args)
    result = cursor.fetchall()

    connect_close(conn, cursor)
    return result


def fetch_one(sql, args=None, c_type=pymysql.cursors.DictCursor):
    """查询单条记录"""
    conn, cursor = connect(c_type)

    cursor.execute(sql, args)
    result = cursor.fetchone()

    connect_close(conn, cursor)
    return result


def insert(sql, args, c_type=pymysql.cursors.DictCursor,):
    """添加数据"""
    conn, cursor = connect(c_type)

    row = cursor.execute(sql, args)
    conn.commit()

    connect_close(conn, cursor)
    return row  # 返回添加的数据行数

