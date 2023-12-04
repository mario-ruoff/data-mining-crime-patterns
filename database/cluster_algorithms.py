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

class SpectralClustering:
    pass

class DBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = []

    def fit(self, X):
        """
        Fit the DBSCAN algorithm on dataset X
        """
        self.labels = [0]*len(X)
        C = 0
        
        for P in range(0, len(X)):
            if not (self.labels[P] == 0):
                continue
            
            NeighborPts = self.region_query(X, P)
            if len(NeighborPts) < self.min_samples:
                self.labels[P] = -1
            else:
                C += 1
                self.grow_cluster(X, P, NeighborPts, C)
        
    def grow_cluster(self, X, P, NeighborPts, C):
        """
        Grow a new cluster with label C from point P.
        """
        self.labels[P] = C
        i = 0
        while i < len(NeighborPts):    
            Pn = NeighborPts[i]
            if self.labels[Pn] == -1:
                self.labels[Pn] = C
            elif self.labels[Pn] == 0:
                self.labels[Pn] = C
                PnNeighborPts = self.region_query(X, Pn)
                if len(PnNeighborPts) >= self.min_samples:
                    NeighborPts = NeighborPts + PnNeighborPts
            i += 1

    def region_query(self, X, P):
        """
        Find neighbors of point P in dataset X
        """
        neighbors = []
        for Pn in range(0, len(X)):
            if np.linalg.norm(X[P] - X[Pn]) < self.eps:
                neighbors.append(Pn)
        return neighbors

    def get_clusters(self):
        """
        Retrieve the cluster labels.
        """
        return self.labels
        
if __name__ == '__main__':
    data = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
    kmeans = KMeans4(3)
    dbscan = DBSCAN(3.0, 2.0)

    cluster_centers, labels = kmeans.fit(data)
    dbscan.fit(data)

    print(cluster_centers)
    print(labels)

    print("")

    print(dbscan.get_clusters())