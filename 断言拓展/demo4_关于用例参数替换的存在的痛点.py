class Test01:
    id = 10
    name = 'musen'
    data = '0011'
    title = 'OK'


params = '{"id": "#id#","name": "#name#","data": "#data#", "title": "#title#","aaa" : 11,"bbb" : 222}'
# 当前存在的问题:用例中每个需要替换的参数都要调用一次replace方法
params = params.replace("#id#", str(Test01.id))
params = params.replace("#name", str(Test01.id))
params = params.replace("#data#", str(Test01.id))
params = params.replace("title#", str(Test01.id))
print(params)
