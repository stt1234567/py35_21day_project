from decimal import Decimal

# python中的浮点数存在精度丢失的问题
print(3.3 - 2.1)
# 注意点:创建Decimal类型数据的时候，传入的数据要是字符串类型
aaa = Decimal('3.3') - Decimal('2.1')
print(aaa)
bbb = Decimal(3.3) - Decimal(2.1)
print(bbb)
# Decimal是python中用来表示浮点数精度的一种数值类型
