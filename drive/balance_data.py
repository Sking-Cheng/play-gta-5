import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
#进一步完善神经网络数据集（平衡数据）

train_data = np.load('training_data.npy')   # 加载数据集到train_data

'''
df = pd.DataFrame(train_data)               # 创建DataFrame
print(df.head())                            # 打印前若干行数据
print(Counter(df[1].apply(str)))            # 将label转为字符串，统计数量，打印
'''

lefts = []
rights = []
forwards = []
# 定义三个空列表，分别是要放入label是左侧，右侧和前进的数据集

shuffle(train_data)
# 对数据集进行打乱顺序，为了使数据失去线性，不会对特定的动作产生偏置值，增强训练的效果

for data in train_data: # 遍历数据集
    img = data[0]       # 图片
    choice = data[1]    # label

    # 将不同的label放入对应的数据集中
    if choice == [1,0,0]:
        lefts.append([img,choice])
    elif choice == [0,1,0]:
        forwards.append([img,choice])
    elif choice == [0,0,1]:
        rights.append([img,choice])
    else:
        print('no matches')


forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]
# 将三个方向的数据集数量保持一致，都和forwards[:len(lefts)][:len(rights)]数量一致（平衡数据的核心）

final_data = forwards + lefts + rights
# 将平衡后的数据集合并
shuffle(final_data)
#再次打乱

np.save('training_data.npy', final_data)
# 保存最终的数据集