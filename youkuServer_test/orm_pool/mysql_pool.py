from DBUtils.PooledDB import PooledDB
import pymysql

POOL = PooledDB(
    creator=pymysql, # 使用链接库的模块
    maxconnections=6, # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2, # 初始化时链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,
    maxshared=3,
    blocking=True,# 连接池中如果没有可用连接后，是否阻塞等待
    maxusage=None,
    setsession=[],# 开始会话前执行的命令
    ping=0,
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'lqm576576',
    database = 'youku',
    charset = 'utf8',
    autocommit = True
)
