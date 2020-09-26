import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
#建立神经网络训练的数据集

'''
output是一个one_hot编码，类别的数量与output长度对应
'''

def keys_to_output(keys):
# 不同按键返回不同的output的编码
    output = [0,0,0]
    # 如果按下A output = [1,0,0]
    if 'A' in keys:
        output[0] = 1
    # 如果按下D output = [0,0,1]
    elif 'D' in keys:
        output[2] = 1
    # 否则output = [0,1,0]
    else:
        output[1] = 1
    return output        # 返回output


file_name = 'training_data.npy'
# 如果这个路径是一个文件加载这个文件并将数据类型转为list,否则返回一个空的数据集
if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():
    # 倒计时
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    paused = False     # 暂停初始值False

    while(True):          # 死循环，除非跳出

        if not paused:            # 如果paused是False往下执行
            screen = grab_screen(region=(0,40,800,640))
            # 截取宽度800 高度600的屏幕图片
            last_time = time.time()
            # 定义一个时间
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # 将图片转成灰度图
            screen = cv2.resize(screen, (160,120))
            # 改变图片大小变成160*120，减小计算量提高帧率
            keys = key_check()
            # 捕获按键信息,返回按下的键
            output = keys_to_output(keys)
            # 设置output作为当前图像的label
            training_data.append([screen,output])
            # 将图像和output添加到数据集中

            if len(training_data) % 1000 == 0:
                # 每1000次保存一次数据集
                print(len(training_data))
                np.save(file_name,training_data)
        keys = key_check()
        # 捕获按键信息,返回按下的键

        if 'T' in keys:
            # 如果按下T，如果当前paused是True,变成False,如果当前是False，变成True，相应的打印出暂停中或未暂停
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)

main()
