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
        # Randomly choose centroids from the data
        copy = np.copy(data)
        np.random.shuffle(copy)
        centroids = copy[:self.k]

        for c in copy:
            pass

    def fit2(self, X, tolerance=1e-4):
        # Step 1: Initialize centroids randomly from the dataset
        centroids = X[np.random.choice(X.shape[0], self.k, replace=False)]

        for _ in range(self.max_iter):
            # Step 2: Assign points to the nearest centroid
            distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
            closest_centroids = np.argmin(distances, axis=0)

            # Step 3: Update centroids to be the mean of assigned points
            new_centroids = np.array([X[closest_centroids == i].mean(axis=0) for i in range(self.k)])

            # Check for convergence (if centroids don't change)
            if np.all(np.abs(new_centroids - centroids) < tolerance):
                for c in centroids:
                    print(f'Centroid: {c}')
                break

            centroids = new_centroids

        return closest_centroids, centroids