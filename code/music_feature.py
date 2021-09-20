# 获取音乐的各种波形特征
import librosa.display
import os
import matplotlib.pyplot as plt
import librosa
import sklearn
from pydub import AudioSegment

def crossingRate(filePath):
    x, sr = librosa.load(filePath)
    n0 = 9000
    n1 = 9100
    plt.figure(figsize=(14, 5))
    plt.plot(x[n0:n1])
    plt.grid()
    zero_crossings = librosa.zero_crossings(x[n0:n1], pad=False)
    return sum(zero_crossings)


# Spectral Centroid
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)
def centroid(filePath,fileName):
    x, sr = librosa.load(filePath)
    spectral_centroids = librosa.feature.spectral_centroid(x, sr=sr)[0]
    print(spectral_centroids)
    # spectral_centroids.shape(775,)
    frames = range(len(spectral_centroids))
    t = librosa.frames_to_time(frames)
    plt.figure(figsize=(20, 5))
    librosa.display.waveplot(x, sr=sr, alpha=0.4)
    plt.plot(t, normalize(spectral_centroids), color='r')
    # plt.savefig(source_path+'/'+fileName.split('.')[0])
    plt.show()

def rolloff(filePath):
    x, sr = librosa.load(filePath)
    spectral_rolloff = librosa.feature.spectral_rolloff(x + 0.01, sr=sr)[0]
    frames = range(len(spectral_rolloff))
    t = librosa.frames_to_time(frames)
    librosa.display.waveplot(x, sr=sr, alpha=0.4)
    plt.plot(t, normalize(spectral_rolloff), color='r')

def amplitude(filePath,fileName):
    x, sr = librosa.load(filePath)
    print(x.shape)
    plt.figure(figsize=(20, 5))
    librosa.display.waveplot(x, sr=sr)
    plt.savefig('../amplitude_img/'+fileName+'.jpg')
    plt.show()

### 获取音乐振幅时间
