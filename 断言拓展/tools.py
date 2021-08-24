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
def replace_data(data,cls):
    """
    :param data:要进行替换的用例数据
    :param cls:测试类
    :return:
    """
    while re.search( "#(.+?)#",data):
        #group():提取匹配对象中的内容
        res2=re.search( "#(.+?)#",data)
        item= res2.group()
        attr = res2.group(1)
        value = getattr(cls,attr)
        #进行替换
        data = data.replace(item, str(value))

    return data

if __name__ == '__main__':

    data=replace_data(s,TestData)
    print(data)