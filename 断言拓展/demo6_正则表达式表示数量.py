import re

# 通过正则表达式的规则，匹配我们需要的数据
# str1 = "ashsdaik13478907890sdah13465455890sdas13466907890dasd"
# res = re.findall( '\d{11}',str1)
# print(res)
"""
正则表达式的语法接介绍
"""
# ---------------表示数量----------------------
s1='1234aanca112233.1234466,123452343242553'
# {n}:表示前一个字符出现n次
#res1 = re.findall( '\d\d\d\d\d',s1)
res1=re.findall('\d{5}',s1)
print(res1)

# {n,}:表示前一个字符出现n次以上
res2=re.findall('\d{5,}',s1)
print(res2)

# {n,m}:表示前一个字符出现n到m次 贪婪模式
res3=re.findall('\d{5,6}',s1)
print(res3)
# {n,m}?:表示前一个字符出现n到m次 贪婪关闭模式
res4=re.findall('\d{5,6}?',s1)
print(res4)
params = '{"id": "#id#","name": "#name#","data": "#data#", "title": "#title#"}'
res5=re.findall('#.{1,}?#',params)
print(res5)
#--------------------------------------------------------
# +:表示1次以上======》等同于{1,}
params = '{"id": "#id#","name": "#name#","data": "#data#", "title": "#title#","aaa":1111,"bb":2343}'
#res5=re.findall('#.{1,}?#',params)
res6=re.findall('#.+?#',params)
print(res6)
#* :表示0次以上
s = '123abc'
res7 = re.findall('\d*',s)
print(res7)
params = '{"id": "##","name": "#name#","data": "#data#", "title": "#title#","aaa":1111,"bb":2343}'
res8=re.findall('#.*?#',params)
print(res8)
html = '<p>pythonasasasas</p><p>python</p><p>1111</p><p>1</p><p></p>'
res9=re.findall('<p>(.*?)</p>',html)
print(res9)
