import pymysql

"""
python3中操作mysql数据库
1、pymysql模块
2.、mysql-client模块:在windows下通过pip安装不了(了解即可，操作和使用都是一样)
"""
# 1、连接数据库
con = pymysql.connect(host='api.lemonban.com',
                      port=3306,
                      user='future',  # The first four arguments is based on DB-API 2.0 recommendation.
                      password='123456',
                      charset='utf8',
                      database='futureloan'
                      )

# 2、创建游标
cur = con.cursor()
# 3、执行sql语句
sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone="13584213498";'
res = cur.execute(sql)
con.commit()
print(res)
#3、a获取查询结果
#fetchall:获取查询集中所有的内容
res =cur.fetchall()

print(res)
cur.close()
# 断开连接
con.close()
