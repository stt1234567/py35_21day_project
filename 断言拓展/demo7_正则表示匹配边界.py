import re
"""
表示边界
字符串边界:
    ^:表示字符串的开头（起始位置)
    $:表示字符串的结尾(终止位置)
单词边界:
\b:表示单词边界
\B:表示非单词边界

"""
#------------------表示边界------------------------
#^:表示字符串的开头（起始位置)
s = '123python456java123c++123'
# res = re.findall('^123',s)
# print(res)
#$:表示字符串的结尾(终止位置)
# res=re.findall('123$',s)
# print(res)
# \b:表示单词边界
# s = 'python ispython good?java'
# res = re.findall(r'\bpython',s)
# print(res)
# \B:表示非单词边界
s = 'python ispython good?java'
res = re.findall(r'\Bpython',s)
print(res)
#注意点:
#python中\b是一个转义字符----->表示键盘上的backspace
# print( ' python\bjava ' )
