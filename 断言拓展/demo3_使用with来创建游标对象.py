import pymysql

"""
python3中操作mysql数据库
1、pymysql模块
2.、mysql-client模块:在windows下通过pip安装不了(了解即可，操作和使用都是一样)
"""
# 1、连接数据库
con = pymysql.connect(host='api.lemonban.com',
                      port=3306,
                      user='future',
                      password='123456',
                      charset='utf8',
                      cursorclass=pymysql.cursors.DictCursor # 设置游标对象返回的数据类型为字典格式（默认元组格式）
                      )
sql = 'SELECT * FROM futureloan.member limit 5;'
# 2、创建一个游标对象（自动提交事务)
with con as cur:
    # execute方法执行完sql，返回的数查询到的数据条数
    res = cur.execute(sql)


print(res)
# res = cur.fetchall()
# print(res)
result=cur.fetchone()
print(result)
cur.close()
# 断开连接
con.close()
"""
with y启动对象上下文管理器的关键字
上下文管理器协议:如果一个类中定义了如下两个方法那么该类就实现了上:下文管理器协议（可以通过with去进行操作)
    __enter__:with XXX as后面的变量接收的是改方法的返回值
    __exit__:with中的代码执行完毕之后会执行该方法
"""
