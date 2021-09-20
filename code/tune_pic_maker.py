import wave
import matplotlib.pyplot as plt
import numpy as np
import os
def pitch(list):
    ans=0
    for i in range(len(list)):
        ans+=(i+1)*abs(list[i])
    ans=ans/len(list)
    return  ans
filepath = "..\\融合wav\\" #添加路径
filename= os.listdir(filepath)
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
for file in filename:
    f = wave.open(filepath+file, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    time = nframes / framerate
    strData = f.readframes(nframes)  # 读取音频，字符串格式
    waveData = np.fromstring(strData, dtype=np.int16)  # 将字符串转化为int
    data = waveData[0::2]
    interval = 8000
    extra = len(data) % interval
    data = data[0:len(data) - extra]
    anslist = []
    for i in range(0, len(data), interval):
        list = data[i:i + interval]
        list = np.fft.rfft(list)
        anslist.append(int(pitch(list)))
    x = np.arange(0, time, time / len(anslist))
    if(len(x)!=len(anslist)):
        continue
    plt.plot(x, anslist)
    plt.title(file+'音调图')
    plt.ylabel('Pitch')
    plt.xlabel('Time(s)')
    plt.savefig('..\\音调图\\'+file+'.png')
    plt.close()
    print(file, "音调变化图已保存")