import matplotlib.pyplot as plt
import numpy as np
import pretty_midi
import os
filepath = "..\\midi\\" #添加路径
filename= os.listdir(filepath)
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
for file in filename:
    filter_size = 256
    standard_deviation = 128
    file_name =filepath+file
    pm = pretty_midi.PrettyMIDI(file_name)
    piano_roll = pm.get_piano_roll(fs=10)
    Tx = len(piano_roll[0])
    x = np.zeros(shape=(128, Tx))
    x[:, :] = piano_roll
    x = np.transpose(x)
    S = np.zeros((Tx, Tx))
    for i in range(Tx):
        S[i] = (np.sum(np.sqrt(np.square(x - x[i])), axis=1))  # 欧氏距离
    plt.figure()
    plt.imshow(S,cmap = plt.get_cmap('hot'),aspect = 'auto')
    plt.title(file)
    plt.savefig('..\\自相似矩阵图\\' + file + '.png')
    plt.close()
    print(file,"自相似矩阵图已保存")