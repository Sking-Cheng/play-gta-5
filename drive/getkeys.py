import win32api as wapi


keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)
#全部注入按键列表keylist中


# 捕获按键函数
def key_check():
    keys = []                 # 定义一个空列表
    for key in keyList:       # 遍历上面字符中所有的字母数字或者符号
        if wapi.GetAsyncKeyState(ord(key)):
            # GetAsyncKeyState函数得到某个键的状态
            # 如果按下了当前的键，将字符存入列表中
            keys.append(key)
    return keys