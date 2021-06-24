# -*- coding: utf-8 -*-
"""
@author: LXA
 Date: 2020 年 5 月 31 日
"""

import tensorflow as tf
import numpy as np
#
# 用于最中执行batch normalization的函数
# tf.nn.batch_normalization(
#     x,
#     mean,
#     variance,
#     offset,
#     scale,
#     variance_epsilon,
#     name=None
# )
#
# 参数：
# x是input输入样本
# mean是样本均值
# variance是样本方差
# offset是样本偏移(相加一个转化值)
# scale是缩放（默认为1）
# variance_epsilon是为了避免分母为0，添加的一个极小值
# 输出的计算公式为：
# y = scale * (x - mean) / var + offset
#
# -------------------------------------------------------
# def moments(
#     x,
#     axes,
#     shift=None,  # pylint: disable=unused-argument
#     name=None,
#     keep_dims=False):
#
# 参数：
# x：一个tensor张量，即我们的输入数据
# axes：一个int型数组，它用来指定我们计算均值和方差的轴（这里不好理解，可以结合下面的例子）
# shift：当前实现中并没有用到
# name：用作计算moment操作的名称
# keep_dims：输出和输入是否保持相同的维度
#
# 返回：
# 两个tensor张量：均值和方差


def mean_var2tensor(input_variable):
    v_shape = input_variable.get_shape()
    axis = [len(v_shape) - 1]
    v_mean, v_var = tf.nn.moments(input_variable, axes=axis, keep_dims=True)
    return v_mean, v_var


def mean_var2numpy(input_variable):
    v_shape = input_variable.get_shape()
    axis = [len(v_shape) - 1]
    v_mean, v_var = tf.nn.moments(input_variable, axes=axis, keep_dims=True)
    return v_mean, v_var


def my_batch_normalization(input_x, is_training=True, name='BatchNorm', moving_decay=0.9):
    # Batch Normalize
    x_shape = input_x.get_shape()
    axis = [len(x_shape) - 1]
    with tf.variable_scope(name):
        x_mean, x_var = tf.nn.moments(input_x, axes=axis, name='moments', keep_dims=True)
        scale = tf.constant(0.1)  # 所有的batch 使用同一个scale因子
        shift = tf.constant(0.001)  # 所有的batch 使用同一个shift项
        epsilon = 0.0001

        # 采用滑动平均更新均值与方差
        ema = tf.train.ExponentialMovingAverage(moving_decay)

        def mean_var_with_update():
            ema_apply_op = ema.apply([x_mean, x_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(x_mean), tf.identity(x_var)

        # 训练时，更新均值与方差，测试时使用之前最后一次保存的均值与方差
        x_mean, x_var = tf.cond(tf.equal(is_training, True), mean_var_with_update,
                                lambda: (ema.average(x_mean), ema.average(x_var)))

        out_x = tf.nn.batch_normalization(input_x, x_mean, x_var, shift, scale, epsilon)
        return out_x


def my_bn(input_x, is_training=True, name='BatchNorm', moving_decay=0.9):
    # Batch Normalize
    x_shape = input_x.get_shape()
    axis = [len(x_shape) - 1]
    with tf.variable_scope(name):
        x_mean, x_var = tf.nn.moments(input_x, axes=axis, name='moments', keep_dims=True)
        scale = tf.constant(0.1)  # 所有的batch 使用同一个scale因子
        shift = tf.constant(0.001)  # 所有的batch 使用同一个shift项
        epsilon = 0.0001
        out_x = tf.nn.batch_normalization(input_x, x_mean, x_var, shift, scale, epsilon)
        return out_x


# ---------------------------------------------- my activations -----------------------------------------------
def mysin(x):
    return tf.sin(2*np.pi*x)


def srelu(x):
    return tf.nn.relu(1-x)*tf.nn.relu(x)


def s2relu(x):
    return tf.nn.relu(1-x)*tf.nn.relu(x)*tf.sin(2*np.pi*x)
    # return 1.5*tf.nn.relu(1-x)*tf.nn.relu(x)*tf.sin(2*np.pi*x)
    # return 1.25*tf.nn.relu(1-x)*tf.nn.relu(x)*tf.sin(2*np.pi*x)


def sinAddcos(x):
    return 0.5*(tf.sin(x) + tf.cos(x))
    # return tf.sin(x) + tf.cos(x)


def sinAddcos_sReLu(x):
    # return tf.nn.relu(1-x)*tf.nn.relu(x)*(tf.sin(2*np.pi*x) + tf.cos(2*np.pi*x))
    return tf.nn.relu(1 - x) * tf.nn.relu(x) * (tf.sin(2 * np.pi * x) + tf.cos(np.pi * x))
    # return tf.sin(x) + tf.cos(x)


def s3relu(x):
    # return 0.5*tf.nn.relu(1-x)*tf.nn.relu(1+x)*tf.sin(2*np.pi*x)
    # return 0.21*tf.nn.relu(1-x)*tf.nn.relu(1+x)*tf.sin(2*np.pi*x)
    # return tf.nn.relu(1 - x) * tf.nn.relu(x) * (tf.sin(2 * np.pi * x) + tf.cos(2 * np.pi * x))   # (work不好)
    # return tf.nn.relu(1 - x) * tf.nn.relu(1 + x) * (tf.sin(2 * np.pi * x) + tf.cos(2 * np.pi * x)) #（不work）
    return tf.nn.relu(1-tf.abs(x))*tf.nn.relu(tf.abs(x))*tf.sin(2*np.pi*tf.abs(x))      # work 不如 s2relu
    # return tf.nn.relu(1-tf.abs(x))*tf.nn.relu(tf.abs(x))*tf.sin(2*np.pi*x)            # work 不如 s2relu
    # return 1.5*tf.nn.relu(1-tf.abs(x))*tf.nn.relu(tf.abs(x))*tf.sin(np.pi*x)
    # return tf.nn.relu(1 - x) * tf.nn.relu(x+0.5) * tf.sin(2 * np.pi * x)


def csrelu(x):
    # return tf.nn.relu(1-x)*tf.nn.relu(x)*tf.cos(np.pi*x)
    return 1.5*tf.nn.relu(1 - x) * tf.nn.relu(x) * tf.cos(np.pi * x)
    # return tf.nn.relu(1-tf.abs(x))*tf.nn.relu(tf.abs(x))*tf.cos(np.pi*x)


def stanh(x):
    # return tf.tanh(x)*tf.sin(2*np.pi*x)
    return tf.sin(2*np.pi*tf.tanh(x))


def gauss(x):
    return 0.2*tf.exp(-4*x*x)
    # return 0.25*tf.exp(-7.5*(x-0.5)*(x-0.5))


def mexican(x):
    return (1-x*x)*tf.exp(-0.5*x*x)


def modify_mexican(x):
    # return 1.25*x*tf.exp(-0.25*x*x)
    # return x * tf.exp(-0.125 * x * x)
    return x * tf.exp(-0.075*x * x)
    # return -1.25*x*tf.exp(-0.25*x*x)


def sm_mexican(x):
    # return tf.sin(np.pi*x) * x * tf.exp(-0.075*x * x)
    # return tf.sin(np.pi*x) * x * tf.exp(-0.125*x * x)
    return 2.0*tf.sin(np.pi*x) * x * tf.exp(-0.5*x * x)


def singauss(x):
    # return 0.6 * tf.exp(-4 * x * x) * tf.sin(np.pi * x)
    # return 0.6 * tf.exp(-5 * x * x) * tf.sin(np.pi * x)
    # return 0.75*tf.exp(-5*x*x)*tf.sin(2*np.pi*x)
    # return tf.exp(-(x-0.5) * (x - 0.5)) * tf.sin(np.pi * x)
    # return 0.25 * tf.exp(-3.5 * x * x) * tf.sin(2 * np.pi * x)
    # return 0.225*tf.exp(-2.5 * (x - 0.5) * (x - 0.5)) * tf.sin(2*np.pi * x)
    return 0.225 * tf.exp(-2 * (x - 0.5) * (x - 0.5)) * tf.sin(2 * np.pi * x)
    # return 0.4 * tf.exp(-10 * (x - 0.5) * (x - 0.5)) * tf.sin(2 * np.pi * x)
    # return 0.45 * tf.exp(-5 * (x - 1.0) * (x - 1.0)) * tf.sin(np.pi * x)
    # return 0.3 * tf.exp(-5 * (x - 1.0) * (x - 1.0)) * tf.sin(2 * np.pi * x)
    # return tf.sin(2*np.pi*tf.exp(-0.5*x*x))


def powsin_srelu(x):
    return tf.nn.relu(1-x)*tf.nn.relu(x)*tf.sin(2*np.pi*x)*tf.sin(2*np.pi*x)


def sin2_srelu(x):
    return 2.0*tf.nn.relu(1-x)*tf.nn.relu(x)*tf.sin(4*np.pi*x)*tf.sin(2*np.pi*x)


def slrelu(x):
    return tf.nn.leaky_relu(1-x)*tf.nn.leaky_relu(x)


def pow2relu(x):
    return tf.nn.relu(1-x)*tf.nn.relu(x)*tf.nn.relu(x)


def selu(x):
    return tf.nn.elu(1-x)*tf.nn.elu(x)


def wave(x):
    return tf.nn.relu(x) - 2*tf.nn.relu(x-1/4) + \
           2*tf.nn.relu(x-3/4) - tf.nn.relu(x-1)


def phi(x):
    return tf.nn.relu(x) * tf.nn.relu(x)-3*tf.nn.relu(x-1)*tf.nn.relu(x-1) + 3*tf.nn.relu(x-2)*tf.nn.relu(x-2) \
           - tf.nn.relu(x-3)*tf.nn.relu(x-3)*tf.nn.relu(x-3)


# ------------------------------------------------  初始化权重和偏置 --------------------------------------------
# 生成DNN的权重和偏置
# tf.random_normal(): 用于从服从指定正太分布的数值中取出随机数
# tf.random_normal(shape,mean=0.0,stddev=1.0,dtype=tf.float32,seed=None,name=None)
# hape: 输出张量的形状，必选.--- mean: 正态分布的均值，默认为0.----stddev: 正态分布的标准差，默认为1.0
# dtype: 输出的类型，默认为tf.float32 ----seed: 随机数种子，是一个整数，当设置之后，每次生成的随机数都一样---name: 操作的名称
def Generally_Init_NN(in_size, out_size, hidden_layers, Flag='flag'):
    n_hiddens = len(hidden_layers)
    Weights = []  # 权重列表，用于存储隐藏层的权重
    Biases = []  # 偏置列表，用于存储隐藏层的偏置
    # 隐藏层：第一层的权重和偏置，对输入数据做变换
    W = tf.Variable(0.1 * tf.random.normal([in_size, hidden_layers[0]]), dtype='float32',
                    name='W_transInput' + str(Flag))
    B = tf.Variable(0.1 * tf.random.uniform([1, hidden_layers[0]]), dtype='float32',
                    name='B_transInput' + str(Flag))
    Weights.append(W)
    Biases.append(B)
    # 隐藏层：第二至倒数第二层的权重和偏置
    for i_layer in range(n_hiddens - 1):
        W = tf.Variable(0.1 * tf.random.normal([hidden_layers[i_layer], hidden_layers[i_layer+1]]), dtype='float32',
                        name='W_hidden' + str(i_layer + 1) + str(Flag))
        B = tf.Variable(0.1 * tf.random.uniform([1, hidden_layers[i_layer+1]]), dtype='float32',
                        name='B_hidden' + str(i_layer + 1) + str(Flag))
        Weights.append(W)
        Biases.append(B)

    # 输出层：最后一层的权重和偏置。将最后的结果变换到输出维度
    W = tf.Variable(0.1 * tf.random.normal([hidden_layers[-1], out_size]), dtype='float32',
                    name='W_outTrans' + str(Flag))
    B = tf.Variable(0.1 * tf.random.uniform([1, out_size]), dtype='float32',
                    name='B_outTrans' + str(Flag))
    Weights.append(W)
    Biases.append(B)

    return Weights, Biases


# tf.truncated_normal(shape, mean, stddev) :shape表示生成张量的维度，mean是均值，stddev是标准差。这个函数产生正太分布，
# 均值和标准差自己设定。这是一个截断的产生正太分布的函数，就是说产生正太分布的值如果与均值的差值大于两倍的标准差，
# 那就重新生成。和一般的正太分布的产生随机数据比起来，这个函数产生的随机数与均值的差距不会超过两倍的标准差，但是一般的别的函数是可能的。
# truncated_normal(
#     shape,
#     mean=0.0,
#     stddev=1.0,
#     dtype=tf.float32,
#     seed=None,
#     name=None)
def truncated_normal_init(in_dim, out_dim, scale_coef=1.0, weight_name='weight'):
    xavier_stddev = np.sqrt(2/(in_dim + out_dim))
    # 尺度因子防止初始化的数值太小或者太大
    V = tf.Variable(scale_coef*tf.truncated_normal([in_dim, out_dim], stddev=xavier_stddev), dtype=tf.float32, name=weight_name)
    return V


# tf.random_uniform()
# 默认是在 0 到 1 之间产生随机数，也可以通过 minval 和 maxval 指定上下界
def uniform_init(in_dim, out_dim, weight_name='weight'):
    V = tf.Variable(tf.random_uniform([in_dim, out_dim], dtype=tf.float32), dtype=tf.float32, name=weight_name)
    return V


# tf.random_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
# 从正态分布中输出随机值。
# 参数:
#     shape: 一维的张量，也是输出的张量。
#     mean: 正态分布的均值。
#     stddev: 正态分布的标准差。
#     dtype: 输出的类型。
#     seed: 一个整数，当设置之后，每次生成的随机数都一样。
#     name: 操作的名字。
def normal_init(in_dim, out_dim, scale_coef=1.0, weight_name='weight'):
    stddev2normal = np.sqrt(2.0/(in_dim + out_dim))
    # 尺度因子防止初始化的数值太小或者太大
    V = tf.Variable(scale_coef*tf.random_normal([in_dim, out_dim], mean=0, stddev=stddev2normal, dtype=tf.float32),
                    dtype=tf.float32, name=weight_name)
    return V


def Truncated_normal_init_NN(in_size, out_size, hidden_layers, Flag='flag'):
    with tf.variable_scope('WB_scope', reuse=tf.AUTO_REUSE):
        scale = 5.0
        n_hiddens = len(hidden_layers)
        Weights = []                  # 权重列表，用于存储隐藏层的权重
        Biases = []                   # 偏置列表，用于存储隐藏层的偏置

        # 隐藏层：第一层的权重和偏置，对输入数据做变换
        W = truncated_normal_init(in_size, hidden_layers[0], scale_coef=scale, weight_name='W-transInput' + str(Flag))
        B = uniform_init(1, hidden_layers[0], weight_name='B-transInput' + str(Flag))
        Weights.append(W)
        Biases.append(B)
        for i_layer in range(0, n_hiddens - 1):
            W = truncated_normal_init(hidden_layers[i_layer], hidden_layers[i_layer + 1], scale_coef=scale,
                                      weight_name='W-hidden' + str(i_layer + 1) + str(Flag))
            B = uniform_init(1, hidden_layers[i_layer + 1], weight_name='B-hidden' + str(i_layer + 1) + str(Flag))
            Weights.append(W)
            Biases.append(B)

        # 输出层：最后一层的权重和偏置。将最后的结果变换到输出维度
        W = truncated_normal_init(hidden_layers[-1], out_size, scale_coef=scale, weight_name='W-outTrans' + str(Flag))
        B = uniform_init(1, out_size, weight_name='B-outTrans' + str(Flag))
        Weights.append(W)
        Biases.append(B)
        return Weights, Biases


def Xavier_init_NN(in_size, out_size, hidden_layers, Flag='flag', varcoe=0.5):
    with tf.variable_scope('WB_scope', reuse=tf.AUTO_REUSE):
        n_hiddens = len(hidden_layers)
        Weights = []  # 权重列表，用于存储隐藏层的权重
        Biases = []  # 偏置列表，用于存储隐藏层的偏置
        # 隐藏层：第一层的权重和偏置，对输入数据做变换
        stddev_WB = (2.0 / (in_size + hidden_layers[0])) ** varcoe
        W = tf.get_variable(name='W-transInput' + str(Flag), shape=(in_size, hidden_layers[0]),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB),
                            dtype=tf.float32)
        B = tf.get_variable(name='B-transInput' + str(Flag), shape=(hidden_layers[0],),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB),
                            dtype=tf.float32)
        Weights.append(W)
        Biases.append(B)
        for i_layer in range(0, n_hiddens - 1):
            stddev_WB = (2.0 / (hidden_layers[i_layer] + hidden_layers[i_layer + 1])) ** varcoe
            W = tf.get_variable(
                name='W' + str(i_layer + 1) + str(Flag), shape=(hidden_layers[i_layer], hidden_layers[i_layer + 1]),
                initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
            B = tf.get_variable(name='B' + str(i_layer + 1) + str(Flag), shape=(hidden_layers[i_layer + 1],),
                                initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
            Weights.append(W)
            Biases.append(B)

        # 输出层：最后一层的权重和偏置。将最后的结果变换到输出维度
        stddev_WB = (2.0 / (hidden_layers[-1] + out_size)) ** varcoe
        W = tf.get_variable(name='W-outTrans' + str(Flag), shape=(hidden_layers[-1], out_size),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
        B = tf.get_variable(name='B-outTrans' + str(Flag), shape=(out_size,),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)

        Weights.append(W)
        Biases.append(B)
        return Weights, Biases


def Xavier_init_NN_Fourier(in_size, out_size, hidden_layers, Flag='flag', varcoe=0.5):
    with tf.variable_scope('WB_scope', reuse=tf.AUTO_REUSE):
        n_hiddens = len(hidden_layers)
        Weights = []  # 权重列表，用于存储隐藏层的权重
        Biases = []  # 偏置列表，用于存储隐藏层的偏置
        # 隐藏层：第一层的权重和偏置，对输入数据做变换
        stddev_WB = (2.0 / (in_size + hidden_layers[0])) ** varcoe
        W = tf.get_variable(name='W-transInput' + str(Flag), shape=(in_size, hidden_layers[0]),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB),
                            dtype=tf.float32)
        B = tf.get_variable(name='B-transInput' + str(Flag), shape=(hidden_layers[0],),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB),
                            dtype=tf.float32)
        Weights.append(W)
        Biases.append(B)

        for i_layer in range(0, n_hiddens - 1):
            stddev_WB = (2.0 / (hidden_layers[i_layer] + hidden_layers[i_layer + 1])) ** varcoe
            if 0 == i_layer:
                W = tf.get_variable(
                    name='W' + str(i_layer + 1) + str(Flag), shape=(hidden_layers[i_layer]*2, hidden_layers[i_layer + 1]),
                    initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
                B = tf.get_variable(name='B' + str(i_layer + 1) + str(Flag), shape=(hidden_layers[i_layer + 1],),
                                    initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
            else:
                W = tf.get_variable(
                    name='W' + str(i_layer + 1) + str(Flag), shape=(hidden_layers[i_layer], hidden_layers[i_layer + 1]),
                    initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
                B = tf.get_variable(name='B' + str(i_layer + 1) + str(Flag), shape=(hidden_layers[i_layer + 1],),
                                    initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
            Weights.append(W)
            Biases.append(B)

        # 输出层：最后一层的权重和偏置。将最后的结果变换到输出维度
        stddev_WB = (2.0 / (hidden_layers[-1] + out_size)) ** varcoe
        W = tf.get_variable(name='W-outTrans' + str(Flag), shape=(hidden_layers[-1], out_size),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)
        B = tf.get_variable(name='B-outTrans' + str(Flag), shape=(out_size,),
                            initializer=tf.random_normal_initializer(stddev=stddev_WB), dtype=tf.float32)

        Weights.append(W)
        Biases.append(B)
        return Weights, Biases


# ----------------------------------- 正则化 -----------------------------------------------
def regular_weights_biases_L1(weights, biases):
    # L1正则化权重和偏置
    layers = len(weights)
    regular_w = 0
    regular_b = 0
    for i_layer1 in range(layers):
        regular_w = regular_w + tf.reduce_sum(tf.abs(weights[i_layer1]), keep_dims=False)
        regular_b = regular_b + tf.reduce_sum(tf.abs(biases[i_layer1]), keep_dims=False)
    return regular_w + regular_b


# L2正则化权重和偏置
def regular_weights_biases_L2(weights, biases):
    layers = len(weights)
    regular_w = 0
    regular_b = 0
    for i_layer1 in range(layers):
        regular_w = regular_w + tf.reduce_sum(tf.square(weights[i_layer1]), keep_dims=False)
        regular_b = regular_b + tf.reduce_sum(tf.square(biases[i_layer1]), keep_dims=False)
    return regular_w + regular_b


#  --------------------------------------------  网络模型 ------------------------------------------------------
def DNN(variable_input, Weights, Biases, hiddens, activate_name=None):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    layers = len(hiddens) + 1               # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层
    hidden_record = 0
    for k in range(layers-1):
        H_pre = H
        W = Weights[k]
        B = Biases[k]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k] == hidden_record:
            H = H+H_pre
        hidden_record = hiddens[k]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def DNN_BN(variable_input, Weights, Biases, hiddens, activate_name=None, is_training=None):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    layers = len(hiddens) + 1  # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层
    hidden_record = 0
    for k in range(layers-1):
        H_pre = H
        W = Weights[k]
        B = Biases[k]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k] == hidden_record:
            H = H+H_pre
        H = my_bn(H, is_training)
        hidden_record = hiddens[k]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def DNN_scale(variable_input, Weights, Biases, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    Unit_num = int(hiddens[0] / len(freq_frag))

    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    mixcoe = np.repeat(freq_frag, Unit_num)

    # 这个的作用是什么？
    if repeat_Highfreq==True:
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[-1]))
    else:
        mixcoe = np.concatenate((np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[0], mixcoe))

    mixcoe = mixcoe.astype(np.float32)

    layers = len(hiddens) + 1  # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层
    W_in = Weights[0]
    B_in = Biases[0]
    if len(freq_frag) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
    else:
        H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)

    H = DNN_activation(H)

    hidden_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k+1] == hidden_record:
            H = H + H_pre
        hidden_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def subDNNs_scale(variable_input, Wlists, Blists, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi
    elif str.lower(activate_name) == 'scsrelu':
        DNN_activation = sinAddcos_sReLu

    freqs_parts = []
    N2subnets = len(Wlists)
    len2parts = int(len(freq_frag) / N2subnets)
    for isubnet in range(N2subnets - 1):
        part2freq_frag = freq_frag[isubnet * len2parts:len2parts * (isubnet + 1)]
        freqs_parts.append(part2freq_frag)
    part2freq_frag = freq_frag[len2parts * (isubnet + 1):]
    freqs_parts.append(part2freq_frag)

    output = []
    layers = len(hiddens) + 1  # 得到输入到输出的层数，即隐藏层层数
    for isubnet in range(N2subnets):
        len2unit = int(hiddens[0] / len(freqs_parts[isubnet]))

        # Units_num.append(len2unit)
        # np.repeat(a, repeats, axis=None)
        # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
        # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
        mixcoe = np.repeat(freqs_parts[isubnet], len2unit)

        # 这个的作用是什么？
        if repeat_Highfreq == True:
            mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - len2unit * len(freqs_parts[isubnet])]) *
                                     (freqs_parts[isubnet])[-1]))
        else:
            mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - len2unit * len(freqs_parts[isubnet])]) *
                                     (freqs_parts[isubnet])[0]))

        mixcoe = mixcoe.astype(np.float32)

        Weights = Wlists[isubnet]
        Biases = Blists[isubnet]

        H = variable_input  # 代表输入数据，即输入层
        W_in = Weights[0]
        B_in = Biases[0]
        if len(freq_frag) == 1:
            H = tf.add(tf.matmul(H, W_in), B_in)
        else:
            H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)

        H = DNN_activation(H)

        hidden_record = hiddens[0]
        for k in range(layers-2):
            H_pre = H
            W = Weights[k+1]
            B = Biases[k+1]
            H = DNN_activation(tf.add(tf.matmul(H, W), B))
            if hiddens[k+1] == hidden_record:
                H = H + H_pre
            hidden_record = hiddens[k+1]

        W_out = Weights[-1]
        B_out = Biases[-1]
        output2subnet = tf.add(tf.matmul(H, W_out), B_out)
        output.append(output2subnet)
    # out = tf.reduce_mean(output, axis=-1)
    # out = tf.reduce_mean(output, axis=0)
    out = tf.reduce_sum(output, axis=0)
    return out


def DNN_adapt_scale(variable_input, Weights, Biases, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    Unit_num = int(hiddens[0] / len(freq_frag))

    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    init_mixcoe = np.repeat(freq_frag, Unit_num)

    # 这个的作用是什么？
    if repeat_Highfreq==True:
        init_mixcoe = np.concatenate((init_mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[-1]))
    else:
        init_mixcoe = np.concatenate((init_mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[0]))

    # 将 int 型的 mixcoe 转化为 发np.flost32 型的 mixcoe，mixcoe[: units[1]]省略了行的维度
    init_mixcoe = init_mixcoe.astype(np.float32)

    layers = len(hiddens)+1                   # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层
    W_in = Weights[0]
    B_in = Biases[0]
    mixcoe = tf.get_variable(name='M0', initializer=init_mixcoe)
    # mixcoe = tf.exp(mixcoe)

    if len(freq_frag) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
    else:
        H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)

    H = DNN_activation(H)

    hidden_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k+1] == hidden_record:
            H = H + H_pre
        hidden_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def subDNNs_adapt_scale(variable_input, Wlists, Blists, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    freqs_parts = []
    N2subnets = len(Wlists)
    len2parts = int(len(freq_frag) / N2subnets)
    for isubnet in range(N2subnets - 1):
        part2freq_frag = freq_frag[isubnet * len2parts:len2parts * (isubnet + 1)]
        freqs_parts.append(part2freq_frag)
    part2freq_frag = freq_frag[len2parts * (isubnet + 1):]
    freqs_parts.append(part2freq_frag)

    output = []
    layers = len(hiddens) + 1  # 得到输入到输出的层数，即隐藏层层数
    for isubnet in range(N2subnets):
        len2unit = int(hiddens[0] / len(freqs_parts[isubnet]))

        # Units_num.append(len2unit)
        # np.repeat(a, repeats, axis=None)
        # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
        # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
        init_mixcoe = np.repeat(freqs_parts[isubnet], len2unit)

        # 这个的作用是什么？
        init_mixcoe = np.concatenate((init_mixcoe, np.ones([hiddens[0] - len2unit * len(freqs_parts[isubnet])]) *
                                     (freqs_parts[isubnet])[-1]))
        init_mixcoe = init_mixcoe.astype(np.float32)

        mixcoe = tf.get_variable(name='M' + str(isubnet), initializer=init_mixcoe)

        Weights = Wlists[isubnet]
        Biases = Blists[isubnet]

        H = variable_input  # 代表输入数据，即输入层
        W_in = Weights[0]
        B_in = Biases[0]
        if len(freq_frag) == 1:
            H = tf.add(tf.matmul(H, W_in), B_in)
        else:
            H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)

        H = DNN_activation(H)

        hidden_record = hiddens[0]
        for k in range(layers-2):
            H_pre = H
            W = Weights[k+1]
            B = Biases[k+1]
            H = DNN_activation(tf.add(tf.matmul(H, W), B))
            if hiddens[k+1] == hidden_record:
                H = H + H_pre
            hidden_record = hiddens[k+1]

        W_out = Weights[-1]
        B_out = Biases[-1]
        output2subnet = tf.add(tf.matmul(H, W_out), B_out)
        output.append(output2subnet)
    out = tf.reduce_mean(output, axis=0)
    return out


def DNN_SinAddCos(variable_input, Weights, Biases, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    layers = len(hiddens) + 1                   # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层

    # 计算第一个隐藏单元和尺度标记的比例
    Unit_num = int(hiddens[0] / len(freq_frag))


    # 然后，频率标记按按照比例复制
    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    mixcoe = np.repeat(freq_frag, Unit_num)

    if repeat_Highfreq == True:
        # 如果第一个隐藏单元的长度大于复制后的频率标记，那就按照最大的频率在最后补齐
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[-1]))
    else:
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[0]))

    mixcoe = mixcoe.astype(np.float32)

    W_in = Weights[0]
    B_in = Biases[0]
    if len(freq_frag) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
    else:
        # H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)
        H = tf.matmul(H, W_in) * mixcoe
    H = 0.5*(tf.sin(H) + tf.cos(H))       # 这样效果才好
    # H = 0.5 * (tf.sin(np.pi*H) + tf.cos(np.pi*H))             # 这样激活，结果会变得糟糕
    # H = 0.5 * (tf.sin(2*(np.pi) * H) + tf.cos(2*(np.pi) * H)) # 这样激活，结果会变得糟糕

    hiddens_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k+1] == hiddens_record:
            H = H+H_pre
        hiddens_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def subDNNs_SinAddCos(variable_input, Wlists, Blists, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    freqs_parts = []
    N2subnets = len(Wlists)
    len2parts = int(len(freq_frag) / N2subnets)
    for isubnet in range(N2subnets - 1):
        part2freq_frag = freq_frag[isubnet * len2parts:len2parts * (isubnet + 1)]
        freqs_parts.append(part2freq_frag)
    part2freq_frag = freq_frag[len2parts * (isubnet + 1):]
    freqs_parts.append(part2freq_frag)

    output = []
    layers = len(hiddens) + 1  # 得到输入到输出的层数，即隐藏层层数
    for isubnet in range(N2subnets):
        len2unit = int(hiddens[0] / len(freqs_parts[isubnet]))

        # Units_num.append(len2unit)
        # np.repeat(a, repeats, axis=None)
        # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
        # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
        init_mixcoe = np.repeat(freqs_parts[isubnet], len2unit)

        # 这个的作用是什么？
        init_mixcoe = np.concatenate((init_mixcoe, np.ones([hiddens[0] - len2unit * len(freqs_parts[isubnet])]) *
                                      (freqs_parts[isubnet])[-1]))
        init_mixcoe = init_mixcoe.astype(np.float32)

        mixcoe = tf.get_variable(name='M' + str(isubnet), initializer=init_mixcoe)

        Weights = Wlists[isubnet]
        Biases = Blists[isubnet]

        H = variable_input                # 代表输入数据，即输入层
        W_in = Weights[0]
        B_in = Biases[0]
        if len(freqs_parts[isubnet]) == 1:
            H = tf.add(tf.matmul(H, W_in), B_in)
        else:
            H = tf.add(tf.matmul(H, W_in) * mixcoe, B_in)

        H = 0.5*(tf.sin(H) + tf.cos(H))    # 这样效果才好
        # H = 0.5 * (tf.sin(np.pi*H) + tf.cos(np.pi*H))  # 这样激活，结果会变得糟糕

        hidden_record = hiddens[0]
        for k in range(layers - 2):
            H_pre = H
            W = Weights[k + 1]
            B = Biases[k + 1]
            H = DNN_activation(tf.add(tf.matmul(H, W), B))
            if hiddens[k + 1] == hidden_record:
                H = H + H_pre
            hidden_record = hiddens[k + 1]

        W_out = Weights[-1]
        B_out = Biases[-1]
        output2subnet = tf.add(tf.matmul(H, W_out), B_out)
        output.append(output2subnet)
    out = tf.reduce_mean(output, axis=0)
    return out


def DNN_Sine0rCos_Base(variable_input, Weights, Biases, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    layers = len(hiddens) + 1                   # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层

    # 计算第一个隐藏单元和尺度标记的比例
    Unit_num = int(hiddens[0] / len(freq_frag))

    # 然后，频率标记按按照比例复制
    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    mixcoe = np.repeat(freq_frag, Unit_num)

    if repeat_Highfreq == True:
        # 如果第一个隐藏单元的长度大于复制后的频率标记，那就按照最大的频率在最后补齐
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[-1]))
    else:
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[0]))

    mixcoe = mixcoe.astype(np.float32)

    W_in = Weights[0]
    B_in = Biases[0]
    if len(freq_frag) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
    else:
        # H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)
        H = tf.matmul(H, W_in) * mixcoe

    if str.lower(activate_name) == 's2relu':
        H = tf.sin(H)
    elif str.lower(activate_name) == 'csrelu':
        H = tf.cos(H)

    hiddens_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k+1] == hiddens_record:
            H = H+H_pre
        hiddens_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


# FourierBase 代表 cos concatenate sin according to row（i.e. the number of sampling points）
def DNN_FourierBase(variable_input, Weights, Biases, hiddens, freq_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi
    elif str.lower(activate_name) == 'sinaddcos':
        DNN_activation = sinAddcos
    elif str.lower(activate_name) == 'scsrelu':
        DNN_activation = sinAddcos_sReLu

    layers = len(hiddens) + 1                   # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层

    # 计算第一个隐藏单元和尺度标记的比例
    Unit_num = int(hiddens[0] / len(freq_frag))

    # 然后，频率标记按按照比例复制
    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    mixcoe = np.repeat(freq_frag, Unit_num)

    if repeat_Highfreq == True:
        # 如果第一个隐藏单元的长度大于复制后的频率标记，那就按照最大的频率在最后补齐
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[-1]))
    else:
        mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(freq_frag)]) * freq_frag[0]))

    mixcoe = mixcoe.astype(np.float32)

    W_in = Weights[0]
    B_in = Biases[0]
    if len(freq_frag) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
    else:
        # H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)
        H = tf.matmul(H, W_in) * mixcoe

    if str.lower(activate_name) == 'tanh':
        sfactor = 1.0
    elif str.lower(activate_name) == 's2relu':
        sfactor = 0.5
    elif str.lower(activate_name) == 'sinaddcos':
        sfactor = 0.5
    else:
        sfactor = 1.0

    H = sfactor * (tf.concat([tf.cos(H), tf.sin(H)], axis=1))  # sfactor=0.5 效果好
    # H = sfactor * (tf.concat([tf.cos(np.pi * H), tf.sin(np.pi * H)], axis=1))
    # H = sfactor * tf.concat([tf.cos(2 * np.pi * H), tf.sin(2 * np.pi * H)], axis=1)

    hiddens_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        W_shape = W.get_shape().as_list()
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if (hiddens[k+1] == hiddens_record) and (W_shape[0] == hiddens_record):
            H = H + H_pre
        hiddens_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def DNN_FourierBase2(variable_input, Weights, Biases, hiddens, freq_frag1, freq_frag2, activate_name=None,
                     repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi
    elif str.lower(activate_name) == 'sinaddcos':
        DNN_activation = sinAddcos

    layers = len(hiddens) + 1                   # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                      # 代表输入数据，即输入层

    # 计算第一个隐藏单元和尺度标记的比例
    Unit_num1 = int(hiddens[0] / len(freq_frag1))
    Unit_num2 = int(int(2)*hiddens[0] / len(freq_frag2))

    # 然后，频率标记按按照比例复制
    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    mixcoe1 = np.repeat(freq_frag1, Unit_num1)
    mixcoe2 = np.repeat(freq_frag2, Unit_num2)

    if repeat_Highfreq == True:
        # 如果第一个隐藏单元的长度大于复制后的频率标记，那就按照最大的频率在最后补齐
        mixcoe1 = np.concatenate((mixcoe1, np.ones([hiddens[0] - Unit_num1 * len(freq_frag1)]) * freq_frag1[-1]))
        mixcoe2 = np.concatenate((mixcoe2, np.ones([int(2)*hiddens[0] - Unit_num2 * len(freq_frag2)]) * freq_frag2[-1]))
    else:
        mixcoe1 = np.concatenate((mixcoe1, np.ones([hiddens[0] - Unit_num1 * len(freq_frag1)]) * freq_frag1[0]))
        mixcoe2 = np.concatenate((mixcoe2, np.ones([int(2)*hiddens[0] - Unit_num2 * len(freq_frag2)]) * freq_frag2[0]))

    mixcoe1 = mixcoe1.astype(np.float32)
    mixcoe2 = mixcoe2.astype(np.float32)

    W_in = Weights[0]
    B_in = Biases[0]
    if len(freq_frag1) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
    else:
        # H = tf.add(tf.matmul(H, W_in)*mixcoe, B_in)
        H = tf.matmul(H, W_in) * mixcoe1

    if str.lower(activate_name) == 'tanh':
        sfactor =1.0
    elif str.lower(activate_name) == 's2relu':
        sfactor = 0.5
    elif str.lower(activate_name) == 'sinaddcos':
        sfactor = 0.5
    else:
        sfactor = 1.0

    H = sfactor * (tf.concat([tf.cos(H), tf.sin(H)], axis=1))  # sfactor=0.5 效果好
    # H = sfactor * (tf.concat([tf.cos(np.pi * H), tf.sin(np.pi * H)], axis=1))
    # H = sfactor * tf.concat([tf.cos(2 * np.pi * H), tf.sin(2 * np.pi * H)], axis=1)

    hiddens_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        W_shape = W.get_shape().as_list()
        if k == 0:
            H = tf.add(tf.matmul(tf.multiply(H, mixcoe2), W), B)
            # H = 0.5*(tf.sin(H) + tf.cos(H))
            H = DNN_activation(H)
        else:
            H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if (hiddens[k+1] == hiddens_record) and (W_shape[0] == hiddens_record):
            H = H + H_pre
        hiddens_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output


def DNN_WaveletBase(variable_input, Weights, Biases, hiddens, scale_frag, activate_name=None, repeat_Highfreq=True):
    if str.lower(activate_name) == 'relu':
        DNN_activation = tf.nn.relu
    elif str.lower(activate_name) == 'leaky_relu':
        DNN_activation = tf.nn.leaky_relu(0.2)
    elif str.lower(activate_name) == 'srelu':
        DNN_activation = srelu
    elif str.lower(activate_name) == 's2relu':
        DNN_activation = s2relu
    elif str.lower(activate_name) == 's3relu':
        DNN_activation = s3relu
    elif str.lower(activate_name) == 'csrelu':
        DNN_activation = csrelu
    elif str.lower(activate_name) == 'sin2_srelu':
        DNN_activation = sin2_srelu
    elif str.lower(activate_name) == 'powsin_srelu':
        DNN_activation = powsin_srelu
    elif str.lower(activate_name) == 'slrelu':
        DNN_activation = slrelu
    elif str.lower(activate_name) == 'elu':
        DNN_activation = tf.nn.elu
    elif str.lower(activate_name) == 'selu':
        DNN_activation = selu
    elif str.lower(activate_name) == 'sin':
        DNN_activation = mysin
    elif str.lower(activate_name) == 'tanh':
        DNN_activation = tf.nn.tanh
    elif str.lower(activate_name) == 'sintanh':
        DNN_activation = stanh
    elif str.lower(activate_name) == 'gauss':
        DNN_activation = gauss
    elif str.lower(activate_name) == 'singauss':
        DNN_activation = singauss
    elif str.lower(activate_name) == 'mexican':
        DNN_activation = mexican
    elif str.lower(activate_name) == 'modify_mexican':
        DNN_activation = modify_mexican
    elif str.lower(activate_name) == 'sin_modify_mexican':
        DNN_activation = sm_mexican
    elif str.lower(activate_name) == 'phi':
        DNN_activation = phi

    layers = len(hiddens) + 1                   # 得到输入到输出的层数，即隐藏层层数
    H = variable_input                          # 代表输入数据，即输入层

    # 计算第一个隐藏单元和尺度标记的比例
    Unit_num = int(hiddens[0] / len(scale_frag))

    # 然后，频率标记按按照比例复制
    # np.repeat(a, repeats, axis=None)
    # 输入: a是数组,repeats是各个元素重复的次数(repeats一般是个标量,稍复杂点是个list),在axis的方向上进行重复
    # 返回: 如果不指定axis,则将重复后的结果展平(维度为1)后返回;如果指定axis,则不展平
    mixcoe = np.repeat(scale_frag, Unit_num)

    # 如果第一个隐藏单元的长度大于复制后的频率标记，那就按照最大的频率在最后补齐
    mixcoe = np.concatenate((mixcoe, np.ones([hiddens[0] - Unit_num * len(scale_frag)]) * scale_frag[-1]))

    mixcoe = mixcoe.astype(np.float32)

    mixcoe = np.reshape(mixcoe, newshape=(1, -1))

    W_in = Weights[0]
    B_in = Biases[0]
    # shape2W_in = W_in.get_shape().as_list()
    # out_dim2W_in = shape2W_in[-1]
    # range2shift0 = np.arange(0, shape2W_in[-1])
    # range2shift = np.reshape(np.arange(0, shape2W_in[-1]), newshape=(1, -1))
    if len(scale_frag) == 1:
        H = tf.add(tf.matmul(H, W_in), B_in)
        H = tf.exp(-2.5*H*H)
    else:
        H1 = tf.matmul(H, W_in)*mixcoe
        H = 0.75*tf.exp(-10*(H1 - mixcoe)*(H1 - mixcoe))*tf.sin(2*np.pi*H1)

    hiddens_record = hiddens[0]
    for k in range(layers-2):
        H_pre = H
        W = Weights[k+1]
        B = Biases[k+1]
        H = DNN_activation(tf.add(tf.matmul(H, W), B))
        if hiddens[k+1] == hiddens_record:
            H = H+H_pre
        hiddens_record = hiddens[k+1]

    W_out = Weights[-1]
    B_out = Biases[-1]
    output = tf.add(tf.matmul(H, W_out), B_out)
    # 下面这个是输出层
    # output = tf.nn.tanh(output)
    return output
