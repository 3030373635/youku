from orm_pool import mysql_pool
import pymysql

class Mysql:
    def __init__(self):
        self.conn = mysql_pool.POOL.connection()
        self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def select(self, sql, value=None):
        self.cursor.execute(sql, value)
        return self.cursor.fetchall()

    def execute(self, sql, value=None):
        try:
            res = self.cursor.execute(sql, value)
            return res
        except Exception as e:
            print("mysql下execute函数执行出现异常-->", e)
