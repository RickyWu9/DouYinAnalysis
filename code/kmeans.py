# K均值聚类
import numpy as np


class kmeans():
	def __init__(self, k=3, max_iter=500, initCenter='random'):
		self.k = k
		self.max_iter = max_iter
		self.initCenter = initCenter
	# 外部调用
	def fit(self, x):
		m = x.shape[0]
		# 最小距离的索引和其具体值
		clusterArray = np.zeros((m, 2))
		if self.initCenter == 'random':
			centroids = self._randomCenter(x, self.k)
		flag = True
		for _ in range(self.max_iter):
			flag = False
			for i in range(m):
				minIdx = -1
				minDist = np.inf
				for j in range(self.k):
					arrayA = centroids[j, :]
					arrayB = x[i, :]
					distAB = self._calEDist(arrayA, arrayB)
					if distAB < minDist:
						minDist = distAB
						minIdx = j
				if clusterArray[i, 0] != minIdx or clusterArray[i, 1] > minDist ** 2:
					flag = True
					clusterArray[i, :] = minIdx, minDist ** 2
			if not flag:
				break
			for i in range(self.k):
				idx_all = clusterArray[:, 0]
				idx_i = np.nonzero(idx_all==i)[0]
				x_i = x[idx_i]
				centroids[i, :] = np.mean(x_i, axis=0)
		return clusterArray, centroids
	# 欧式距离
	def _calEDist(self, arrayA, arrayB):
		return np.math.sqrt(sum(np.power(arrayA-arrayB, 2)))
	# 曼哈顿距离
	def _calMDist(self, arrayA, arrayB):
		return sum(np.abs(arrayA-arrayB))
	# 随机选取k个质心
	def _randomCenter(self, x, k):
		n = x.shape[1]
		centroids = np.empty((k, n))
		for j in range(n):
			minj = min(x[:, j])
			rangej = float(max(x[:, j] - minj))
			centroids[:, j] = (minj + rangej * np.random.rand(k, 1)).flatten()
		return centroids