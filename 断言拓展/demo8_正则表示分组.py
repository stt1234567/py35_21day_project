import re

class TestData():
    id=123
    name='musen'
    data='1122'
    title='数据传输'
"""
表示分组
（）：
"""
#------------------表示分组------------------------
s = '{"id": "#id#","name": "#name#","data": "#data#", "title": "#title#","aaa":1111,"bb":2343}'
#search:匹配并返回第一个符合规则的匹配对象,没有匹配到返回None

while re.search( "#(.+?)#",s):
    #group():提取匹配对象中的内容
    res2=re.search( "#(.+?)#",s)
    item= res2.group()
    attr = res2.group(1)
    value = getattr(TestData,attr)
    #进行替换
    s = s.replace(item, str(value))
print(s)
