import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization

''' AlexNet将LeNet的思想发扬光大，把CNN的基本原理应用到了很深很宽的网络中。AlexNet主要使用到的新技术点如下。

（1）成功使用ReLU作为CNN的激活函数，并验证其效果在较深的网络超过了Sigmoid，成功解决了Sigmoid在网络较深时的梯度弥散问题。虽然ReLU激活函数在很久之前就被提出了，但是直到AlexNet的出现才将其发扬光大。

（2）训练时使用Dropout随机忽略一部分神经元，以避免模型过拟合。Dropout虽有单独的论文论述，但是AlexNet将其实用化，通过实践证实了它的效果。在AlexNet中主要是最后几个全连接层使用了Dropout。

（3）在CNN中使用重叠的最大池化。此前CNN中普遍使用平均池化，AlexNet全部使用最大池化，避免平均池化的模糊化效果。并且AlexNet中提出让步长比池化核的尺寸小，这样池化层的输出之间会有重叠和覆盖，提升了特征的丰富性。

（4）提出了LRN层，对局部神经元的活动创建竞争机制，使得其中响应比较大的值变得相对更大，并抑制其他反馈较小的神经元，增强了模型的泛化能力。
'''

def alexnet(width, height, lr):
    network = input_data(shape=[None, width, height, 1], name='input')
    # 输入层
    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    # 卷积核数量96也就是输出96个通道，卷积核大小11，步长未4，使用relu激活函数对卷积后的结果进行激活
    network = max_pool_2d(network, 3, strides=2)
    # 最大池化,使用卷积核大小为3步长为2
    network = local_response_normalization(network)
    # 局部响应归一化
    network = conv_2d(network, 256, 5, activation='relu')
    # 输出通道256 卷积核大小5 卷积后使用relu进行激活
    network = max_pool_2d(network, 3, strides=2)
    # 最大池化,使用卷积核大小为3步长为2
    network = local_response_normalization(network)
    # 局部响应归一化
    network = conv_2d(network, 384, 3, activation='relu')
    # 输出通道384 卷积核大小3 卷积后使用relu进行激活
    network = conv_2d(network, 384, 3, activation='relu')
    # 输出通道384 卷积核大小3 卷积后使用relu进行激活
    network = conv_2d(network, 256, 3, activation='relu')
    # 输出通道256 卷积核大小3 卷积后使用relu进行激活
    network = max_pool_2d(network, 3, strides=2)
    # 最大池化,使用卷积核大小为3步长为2
    network = local_response_normalization(network)
    # 局部响应归一化
    network = fully_connected(network, 4096, activation='tanh')
    # 全链接隐藏层，拉伸数据编程二维结构，第一维度batch_size,第二维度是4096数据特征向量,激活函数使用tanh
    network = dropout(network, 0.5)
    # 0.5概率忽略神经元
    network = fully_connected(network, 4096, activation='tanh')
    # 全链接隐藏层，拉伸数据编程二维结构，第一维度batch_size,第二维度是4096数据特征向量,激活函数使用tanh
    network = dropout(network, 0.5)
    # 0.5概率忽略神经元
    network = fully_connected(network, 3, activation='softmax')
    # 全链接输出层，拉伸数据编程二维结构，第一维度batch_size,第二维度是3数据特征向量,激活函数使用softmax
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')
    # 定义模型优化器momentum,损失函数交叉熵


    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    # 创建模型

    return model    # 模型返回