import numpy as np

class KMeans4:
    def __init__(self, data, k):
        # randomly initialize centroids
        self.data = data
        self.centroids = data.copy()
        np.random.shuffle(self.centroids)
        self.centroids = self.centroids[:k]
        