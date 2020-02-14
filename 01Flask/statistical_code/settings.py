from datetime import timedelta
import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection


class Config(object):
    SECRET_KEY = 'links'  # session加盐
    SALT = b'aaa'
    PERMANENT_SESSION_LIFETIME = timedelta(days=3)  # 设置session超时时间
    SESSION_REFRESH_EACH_REQUEST = True  # 每次请求都保存session
    MAX_CONTENT_LENGTH = 1024 * 1024 * 7  # 控制上传文件最大为: 7M  # 超过会报一个413的错误

    POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,  # 一般写4或0
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested,
        #                                                             2 = when a cursor is created,
        #                                                             4 = when a query is executed,
        #                                                             7 = always
        host='127.0.0.1',
        port=3306,
        user='root',
        password='xiaoli',
        database='statistical_code',
        charset='utf8'
    )