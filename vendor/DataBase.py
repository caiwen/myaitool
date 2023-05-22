import pymysql


# 数据库操作类
class DataBase:
    def __init__(self, dbname, dbhost, dbuser, dbpassword, dbport, dbcharset='utf8'):
        self._dbname = dbname
        self._dbhost = dbhost
        self._dbuser = dbuser
        self._dbpassword = dbpassword
        self._dbcharset = dbcharset
        self._dbport = int(dbport)
        self._conn = self.connectMySQL()
        if (self._conn):
            self._cursor = self._conn.cursor()

    # 数据库连接
    def connectMySQL(self):
        conn = False
        try:
            conn = pymysql.connect(host=self._dbhost,
                                   user=self._dbuser,
                                   passwd=self._dbpassword,
                                   db=self._dbname,
                                   port=self._dbport,
                                   cursorclass=pymysql.cursors.DictCursor,
                                   charset=self._dbcharset,
                                   )
        except Exception as e:
            conn = False
        return conn

    # 获取查询结果集
    def fetch_all(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception as e:
                res = False
        return res

    def fetch_one(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchone()
            except Exception as e:
                res = False
        return res

    def execute(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as e:
                flag = False
        return flag

    def insert_row(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                flag = self._cursor.lastrowid
                self._conn.commit()
            except Exception as e:
                flag = False
        return flag

    def update(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception as e:
                flag = False
        return flag

    # 关闭数据库连接
    def close(self):
        if (self._conn):
            try:
                if (type(self._cursor) == 'object'):
                    self._cursor.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except Exception as e:
                raise


if __name__ == '__main__':
    dbBase = DataBase()
    # ret = dbBase.fetch_all('SELECT * FROM request_log LIMIT 10')
    # print(ret)
