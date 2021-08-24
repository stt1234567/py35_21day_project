import pymysql
from common.handle_conf import conf

class HandleDB:
    def __init__(self) -> object:
        self.con = pymysql.connect(host=conf.get('mysql', 'host'),
                                   port=conf.getint('mysql', 'port'),
                                   user=conf.get('mysql', 'user'),
                                   password=conf.get('mysql', 'password'),
                                   charset='utf8',
                                   # cursorclass=pymysql.cursors.DictCursor,  # 设置游标对象返回的数据类型为字典格式（默认元组格式）
                                   )

    def find_all(self, sql):
        """查询所有数据"""
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self, sql):
        """查询一条数据"""
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self, sql):
        """sql执行完之后，返同的数据条数"""
        with self.con as cur:
            res = cur.execute(sql)
        cur.close()
        return res

    def __del__(self):
        self.con.close()


if __name__ == '__main__':
    from common.handle_conf import conf

    sql = "SELECT * FRoM futureloan.member WHERE id<5;"
    db = HandleDB()
    res = db.find_all(sql)
    print(res)
