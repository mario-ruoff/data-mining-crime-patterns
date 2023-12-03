import numpy as np

'''
KMeans4: An self-implemented version of kmeans

This method will utilize similar signitures to the scikit-learn
package: 'KMeans' in order to provide similar results. It will not
be optimized.
'''
class KMeans4:
    def __init__(self, n_clusters, max_iter=300):
        self.k = n_clusters
        self.max_iter = max_iter

    def fit(self, data):
        # copy the data for manipulation
        copy = np.copy(data)

        # Randomly set the cluster centers from points in the set
        n_samples, n_features = copy.shape
        cluster_centroids = copy[np.random.choice(n_samples, self.k, replace=False)]

        for _ in range(self.max_iter):
            # Assign the point to the nerest cluster
            labels = np.array([np.argmin(np.sum((x - cluster_centroids) ** 2, axis=1)) for x in data])

            # update centroids to the mean of the points in the cluster
            for i in range(self.k):
                points = copy[labels == i]
                if points.shape[0] > 0:
                    cluster_centroids[i] = np.mean(points, axis=0)

        return cluster_centroids, labels


class DBSCAN:
    pass
        
if __name__ == '__main__':
    data = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
    kmeans = KMeans4(3)

    cluster_centers, labels = kmeans.fit(data)
    print(cluster_centers)
    print(labels)