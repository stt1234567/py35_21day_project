import os
#os.path.abspath:给顶一个相对路径 获取绝对路径
# #获取当前文件的绝对路径
# res=os.path.abspath(__file__)
#
# print(res)
# # os.path.dirname:获取所在目录的路径
# path1=os.path.dirname(res)
# print(path1)
# base_path=os.path.dirname(path1)
# print(base_path)
base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))