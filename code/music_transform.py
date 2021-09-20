# 实现从mp3到wav的转换

import os
from pydub import AudioSegment
import wave

path = "../音乐" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files: #遍历文件夹
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
          # 读取mp3的波形数据
          sound = AudioSegment.from_file(path+"/"+file, format='MP3')
          # 将读取的波形数据转化为wav
          f = wave.open(file+".wav", 'wb')
          f.setnchannels(1)  # 频道数
          f.setsampwidth(2)  # 量化位数
          f.setframerate(16000)  # 取样频率
          f.setnframes(len(sound._data))  # 取样点数，波形数据的长度
          f.writeframes(sound._data)  # 写入波形数据
          f.close()

