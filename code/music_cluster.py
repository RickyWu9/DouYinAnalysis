# 实现音乐聚类
import os
import wave
import struct
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from kmeans import kmeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



# Function:
# 	读取WAV文件
# Input:
# 	wavname(str): .wav文件名
# 	seconds(int): 提取.wav文件前seconds秒的数据,优先级低
# 	is_entire(bool): 是否提取.wav文件的所有数据,优先级高
# Output(tuple):
# 	如果is_entire为True则返回.wav文件的所有数据+文件参数,
# 	否则返回前seconds秒的数据+文件参数
def read_wav(wavname, seconds, is_entire):
	wavfile = wave.open(wavname)
	params = wavfile.getparams()
	if is_entire is True:
		num = params[3]
		frames = wavfile.readframes(num)
		data = struct.unpack('%dh' % (num), frames)
		wavfile.close()
	else:
		num = int(10000 * seconds)
		if params[3] < num:
			raise ValueError('Wave file is too short...')
		frames = wavfile.readframes(num)
		data = struct.unpack('%dh' % (num*2), frames)
		wavfile.close()
	return data, params


# Function:
#
def TFeatures(x):
	# 均值
	mean = x.mean()
	# 标准差
	std = x.var() ** 0.5
	# 偏态
	skewness = ((x - mean) ** 3).mean() / std ** 3
	# 峰态
	kurtosis = ((x - mean) ** 4).mean() / std ** 4
	return [mean, std, skewness, kurtosis]


# Function:
# 	提取频域特征
def FFeatures(x):
	x = np.array(x)
	x = x.reshape(-1, 5).mean(1)
	fft = np.fft.fft(x)
	fft = fft[2: (fft.size // 2 + 1)]
	fft = abs(fft)
	power = fft.sum()
	fft = np.array_split(fft, 10)
	return [i.sum() / power for i in fft]


# Function:
# 	计算每个音乐文件的特征
def ComputeFeatures(x):
	x = np.array(x)
	fv = []
	# Part1
	xs = x
	diff = xs[1:] - xs[:-1]
	fv.extend(TFeatures(xs))
	fv.extend(TFeatures(diff))
	# Part2
	xs = x.reshape(-1, 10).mean(1)
	diff = xs[1:] - xs[:-1]
	fv.extend(TFeatures(xs))
	fv.extend(TFeatures(diff))
	# Part3
	xs = x.reshape(-1, 100).mean(1)
	diff = xs[1:] - xs[:-1]
	fv.extend(TFeatures(xs))
	fv.extend(TFeatures(diff))
	# Part4
	xs = x.reshape(-1, 1000).mean(1)
	diff = xs[1:] - xs[:-1]
	fv.extend(TFeatures(xs))
	fv.extend(TFeatures(diff))
	# Part5
	fv.extend(FFeatures(x))
	return fv


# Function:
# 	.mp3转.wav
def mp32wav(mp3file, outfile='temp.wav'):
	mpg_cmd = 'mpg123 -w "%s" -r 10000 -m "%s"' % (outfile, mp3file)
	_ = subprocess.call(mpg_cmd)


# Function:
# 	画波形图
def plot_wave(x, params, title):
	x = np.array(x)
	if params[0] == 1:
		t = np.arange(0, len(x)) * (1.0 / params[2])
		plt.title(title)
		plt.plot(t, x, color='blue')
		plt.xlabel('time(seconds)')
		plt.show()
	elif params[0] == 2:
		x.shape = -1, 2
		t = np.arange(0, params[3]) * (1.0 / params[2])
		plt.title(title)
		plt.subplot(211)
		plt.plot(t, x[0], color='blue')
		plt.subplot(212)
		plt.plot(t, x[1], color='green')
		plt.xlabel('time(seconds)')
		plt.show()


# Function:
# 	画聚类结果图,仅支持二维数据
def plot_cluster(x, x_names, k, centroids, clusterArray):
	numSamples, dim = x.shape
	if dim != 2:
		print('[Error]: Only dim=2 supported...')
		return None
	colors1 = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
	if k > len(colors1):
		print('[Error]: Only k<%d supported...' % len(colors1))
		return None
	for i in range(numSamples):
		colorsIdx = int(clusterArray[i, 0])
		plt.plot(x[i, 0], x[i, 1], colors1[colorsIdx])
		plt.text(x[i, 0], x[i, 1], x_names[i])
	colors2 = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
	for i in range(k):
		plt.plot(centroids[i, 0], centroids[i, 1], colors2[i], markersize=12)
		plt.text(centroids[i, 0], centroids[i, 1], 'class%d' % i)
	plt.show()


if __name__ == '__main__':
	tar_path = '../音乐'
	fvs = []
	fvs_names = []
	plt.rcParams['font.sans-serif'] = ['SimHei']
	plt.rcParams['axes.unicode_minus'] = False
	for file in os.listdir(tar_path):
		if file.endswith(".wav"):
			print(os.path.join(tar_path, file))
			x, params = read_wav(os.path.join(tar_path, file),15, False)
			fv = ComputeFeatures(x)
			fv = [fv[8], fv[9], fv[10], fv[13], fv[14], fv[15], fv[16], fv[17], fv[21], fv[24], fv[33], fv[34], fv[35], fv[36], fv[37], fv[38], fv[39], fv[40]]
			fvs_names.append(file.split('_')[-1][:-4])
			fvs.append(fv)
	fvs = np.array(fvs)
	scaler = StandardScaler()
	scaler.fit(fvs)
	fvs = scaler.transform(fvs)
	model_pca = PCA(n_components=2).fit(fvs)
	fvs = model_pca.transform(fvs)
	print(fvs)
	k = 3
	model_kmeans = kmeans(k=k, max_iter=500, initCenter='random')
	clusterArray, centroids = model_kmeans.fit(fvs)
	print(len(centroids))
	plot_cluster(fvs, fvs_names, k, centroids, clusterArray)