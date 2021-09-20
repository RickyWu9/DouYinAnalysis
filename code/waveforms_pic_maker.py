import wave
import matplotlib.pyplot as plt
import numpy as np

import os
filepath = "..\\融合wav\\" #添加路径
filename= os.listdir(filepath)
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
for file in filename:
    f=wave.open(filepath+file,'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)#读取音频，字符串格式
    waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
    waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
    waveData = np.reshape(waveData,[nframes,nchannels])
    # plot the wave
    time = np.arange(0,nframes)*(1.0 / framerate)
    plt.subplot(3,1,1)
    plt.plot(time,waveData[:,0])
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Double channel wavedata")
    plt.grid('on')#标尺，on：有，off:无。
    plt.subplot(3,1,3)
    plt.plot(time,waveData[:,1])
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Double channel wavedata")
    plt.grid('on')#标尺，on：有，off:无。
    plt.savefig('..\\波形图\\' + file + '.png')
    plt.close()
    print(file, "波形图已保存")