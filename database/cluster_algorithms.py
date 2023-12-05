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
    def __init__(self, n_clusters, affinity='rbf', gamma=1.0):
        self.n_clusters = n_clusters
        self.affinity = affinity
        self.gamma = gamma

    def fit(self, data):
        # Compute the affinity matrix
        if self.affinity == 'rbf':
            sq_dists = np.sum((data[:, np.newaxis] - data[np.newaxis, :]) ** 2, axis=-1)
            affinity_matrix = np.exp(-self.gamma * sq_dists)
        else:
            raise ValueError("Unknown affinity type")

        # Construct the Laplacian matrix
        D = np.diag(np.sum(affinity_matrix, axis=1))
        L = D - affinity_matrix

        # Compute the first k eigenvectors
        eigenvalues, eigenvectors = self.compute_eigenvectors(L, self.n_clusters)

        # Transform the data
        X_transformed = eigenvectors.real

        # Cluster using KMeans
        kmeans = KMeans4(self.n_clusters)
        test, labels = kmeans.fit(X_transformed)

        # Calculate the mean of the original data points in each cluster to find the cluster centers
        cluster_centers = np.array([data[labels == i].mean(axis=0) for i in range(self.n_clusters)])

        return cluster_centers, labels

    def compute_eigenvectors(self, L, k):
        # Simple power iteration algorithm for eigenvector computation
        n, _ = L.shape
        eigenvectors = np.random.rand(n, k)
        for _ in range(10):  # number of iterations
            eigenvectors = np.dot(L, eigenvectors)
            eigenvectors = np.apply_along_axis(lambda v: v / np.linalg.norm(v), 0, eigenvectors)
        eigenvalues = np.diag(np.dot(np.dot(eigenvectors.T, L), eigenvectors))
        return eigenvalues, eigenvectors


class DBSCAN:
    def __init__(self, eps=2, min_samples=3):
        self.eps = eps
        self.min_samples = min_samples

    def fit(self, X):
        """
        Fit the DBSCAN algorithm on dataset X
        """
        # Number of points
        n_points = X.shape[0]

        # Labels of the points
        labels = [-1] * n_points

        # Visited points
        visited = [False] * n_points

        # Cluster label
        C = 0

        # Iterate over points
        for P in range(n_points):
            if visited[P]:
                continue

            # Mark point as visited
            visited[P] = True

            # Find neighbors
            neighbors = self.region_query(X, P)

            if len(neighbors) < self.min_samples:
                # Mark as noise
                labels[P] = -1
            else:
                # Start a new cluster
                C += 1
                self.expand_cluster(X, labels, P, neighbors, C, visited)

        cluster_centers = self.calculate_cluster_means(X, labels)
        return cluster_centers, labels

    def expand_cluster(self, X, labels, P, neighbors, C, visited):
        """
        Expand the new cluster with label C from point P.
        """
        labels[P] = C
        i = 0
        while i < len(neighbors):
            Pn = neighbors[i]
            if not visited[Pn]:
                visited[Pn] = True
                PnNeighbors = self.region_query(X, Pn)

                if len(PnNeighbors) >= self.min_samples:
                    neighbors = neighbors + PnNeighbors

            if labels[Pn] == -1:
                labels[Pn] = C
            i += 1

    def region_query(self, X, P):
        """
        Find neighbors of point P in dataset X
        """
        neighbors = []
        for Pn in range(len(X)):
            if np.linalg.norm(X[P] - X[Pn]) < self.eps:
                neighbors.append(Pn)
        return neighbors
    
    def calculate_cluster_means(self, X, labels):
        unique_labels = set(labels)
        if -1 in unique_labels:
            unique_labels.remove(-1)  # Remove noise label if present

        cluster_means = []
        for unique_label in unique_labels:
            # Get all points in this specific cluster
            points_in_cluster = np.array([value for value, label in zip(X, labels) if label == unique_label])
            if len(points_in_cluster) > 0:
                cluster_mean = points_in_cluster.mean(axis=0)
                cluster_means.append(cluster_mean)
            else:
                cluster_means.append(None)  # Handle empty cluster case

        return np.array(cluster_means)
        
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