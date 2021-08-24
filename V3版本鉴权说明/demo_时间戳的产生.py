from time import time
from common.handle_sign import HandleSign
t=int(time())
print('当前时间戳：',t)
#签名的获取
#tokeni前50位+时间戳，然后进行RSA加密
token='fsdahadsdsjhkkmcxcsewqeqweqwyuytuiuyiuixxxxxxxxxxxxaseeeeeeeeqw2321454654645'
data=token[:50]+str(t)

hs=HandleSign()
res=hs.encrypt(data)
print(res)

params = {"timestamp": t, "sign": res}
print(params)