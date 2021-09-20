# 使用机器学习对音乐进行分类
from python_speech_features import mfcc, logfbank
from scipy.io import wavfile
import wave
import glob
import os.path as path
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
import os
import logging


class HMMTrainer(object):
    # 使用4作为component默认值， 可以尝试不同的数， 找到最高得分
    def __init__(self, model_name='GaussianHMM', n_components=4, cov_type='diag', n_iter=1000):
        self.model_name = model_name
        self.n_components = n_components
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []
        if self.model_name == 'GaussianHMM':
            self.model = hmm.GaussianHMM(n_components=self.n_components, covariance_type=self.cov_type,
                                         n_iter=self.n_iter)
        else:
            raise TypeError('Invalid model type')

    def train(self, X):
        np.seterr(all='ignore')
        self.models.append(self.model.fit(X))

    # 获取为止类型音乐在该类型音乐下的相似度品分
    def get_score(self, input_data):
        return self.model.score(input_data)


'''
改变帧数 避免报错 但是生成物很难听
def changeRate(filePath):
    wave_read = wave.open(filePath, 'rb')
    print(wave_read.getframerate())
    signal = wave_read.readframes(-1)
    wave_write = wave.open(filePath, 'wb')
    wave_write.setnchannels(1)
    wave_write.setsampwidth(2)
    wave_write.setframerate(16050)
    wave_write.writeframes(signal)
    wave_write.close()
'''

'''
可以初步得到每个类型第一首音乐的mfcc特征图
def traverseSamples():
    genre_list = ['blues', 'classical', 'jazz', 'country', 'pop', 'rock', 'metal', 'disco', 'hiphop', 'reggae']
    print(len(genre_list))
    figure = plt.figure(figsize=(20, 3))
    for idx, genre in enumerate(genre_list):
        example_data_path = samplesPath + genre
        file_paths = glob.glob(path.join(example_data_path, '*.wav'))
        # 只是遍历每个文件夹下的第一首歌
        sampling_freq, audio = wavfile.read(file_paths[0])
        mfcc_features = mfcc(audio, sampling_freq, nfft=1024)
        print(file_paths[0], mfcc_features.shape[0])
        plt.yscale('linear')
        plt.matshow((mfcc_features.T)[:, :300])
        plt.text(150, -10, genre, horizontalalignment='center', fontsize=20)
    plt.yscale('linear')
    plt.show()
'''


def evaluateHHM():
    hmm_models = []
    input_folder = samplesPath
    for dirname in os.listdir(input_folder):
        # 得到音乐类型
        subfolder = os.path.join(input_folder, dirname)
        if not os.path.isdir(subfolder):
            continue
        # 提取音乐类型
        label = subfolder[subfolder.rfind('/') + 1:]
        X = np.array([])
        y_words = []
        # 遍历该音乐类型文件夹下的所有音乐
        print("读取" + label + "类型样本数据...")
        for filename in [x for x in os.listdir(subfolder) if x.endswith('.wav')][:-1]:
            filepath = os.path.join(subfolder, filename)
            sampling_freq, audio = wavfile.read(filepath)
            # 得到mfcc特征
            mfcc_features = mfcc(audio, sampling_freq)
            if len(X) == 0:
                X = mfcc_features
            else:
                X = np.append(X, mfcc_features, axis=0)
            # Append the label
            y_words.append(label)
        hmm_trainer = HMMTrainer(n_components=4)
        print(label + "类型数据读取完成，" + "开始训练...")
        hmm_trainer.train(X)
        print("训练结束!")
        hmm_models.append((hmm_trainer, label))
        hmm_trainer = None
    return hmm_models


def predict(hmm_models):
    print("开始音乐分类...")
    input_folder = wavesPath
    pred_labels = []
    for dirname in os.listdir(input_folder):
        subfolder = os.path.join(input_folder, dirname)
        if not os.path.isdir(subfolder):
            continue
        for filename in [x for x in os.listdir(subfolder) if x.endswith('.wav')][:-1]:
            filepath = os.path.join(subfolder, filename)
            sampling_freq, audio = wavfile.read(filepath)
            mfcc_features = mfcc(audio, sampling_freq)
            max_score = -99999999999999
            output_label = None
            for item in hmm_models:
                hmm_model, label = item
                score = hmm_model.get_score(mfcc_features)
                if score > max_score:
                    max_score = score
                    output_label = label
            pred_labels.append(output_label)
            # print(filename + ": " + output_label)
            result.get(output_label).append(filename)


samplesPath = '../genres/'
wavesPath = '../wav'
result = {"pop": [], "metal": [], "disco": [], "blues": [], "reggae": [], "classical": [], "rock": [], "hiphop": [],
          "country": [], "jazz": []}
if __name__ == '__main__':
    # test()
    # traverseSamples()
    # 设置日志等级，避免控制台无用warning输出
    logging.getLogger().setLevel(logging.ERROR)
    models = evaluateHHM()
    predict(models)
    name_list = []
    num_list = []
    print(result)
    for key in result:
        print(key + "类型有", len(result.get(key)), "首歌")
        name_list.append(key)
        num_list.append(len(result.get(key)))
    plt.bar(name_list, num_list, color='green')
    plt.title("音乐流派统计")
    plt.xlabel("音乐流派")
    plt.ylabel("歌曲数量")
    plt.show()
