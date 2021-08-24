import os

# os.path.abspath:给定一个相对路径 获取绝对路径
# p1=os.path.abspath('code.txt')
# print(p1)
# p2=os.path.abspath('..')
# print(p2)

n = __name__
fp = __file__
print(n)
print(fp)
'''
魔法变量:变量的值在不同的情况下是不一样的
__name__:
    启动文件中的__name__的值为:__main__
    不是启动文件的情况下:打印的值为模块名
    
__file__:代表当前文件的文件名字（pycharm中运行的时候会显示文件的绝对路径)
'''