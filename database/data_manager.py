import numpy as np
import sqlite3

from database.cluster_algorithms import KMeans4, DBSCAN, SpectralClustering

class ChicagoCrimes:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.current_results = []
        self.num_clusters = 0
        
    def get_police_stations(self):

        # something something database
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()

        query = '''
            SELECT latitude,longitude from police
            '''
        
        self.current_results = []
        raw_results = cursor.execute(query)
        result = raw_results.fetchone()
        while(result is not None):
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()

        self.num_clusters = len(self.current_results)
        return self.current_results
    
    def get_crimes(self, k=2, crime_types=None, year=2023, algorithm=1):
        crime_types_string = ', '.join(f"'{x}'" for x in crime_types)
        
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()
        query = f'''
            SELECT latitude,longitude, date, primary_type from crimes
            WHERE primary_type IN ({crime_types_string}) AND year={year}
            ORDER BY random()
            LIMIT 200
            '''
        
        # Get crimes into numpy array
        self.current_results = []
        raw_results = cursor.execute(query)
        result = raw_results.fetchone()
        
        # Abort appending if no results
        if result is None:
            return self.current_results, np.array([])

        # Append results to array
        while(result is not None):
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()
        
        record_array = np.array(self.current_results)
        locations = record_array[:, (0,1)]
        print(len(locations))

        # Abort clustering if not enough results
        if len(locations) < k:
            return self.current_results, np.array([])

        # Convert lat/lng to meters for clustering
        converted_locations = self.lat_lng_to_meters(locations)

        #Apply clustering
        match algorithm:
            case 1:
                model = KMeans4(n_clusters=k)
            case 2:
                model = SpectralClustering(n_clusters=k)
            case 3:
                model = DBSCAN()
            case _:
                model = KMeans4(n_clusters=k)
        converted_clusters, _ = model.fit(converted_locations)

        # Convert centroids back to lat/lng
        clusters = self.meters_to_lat_lng(converted_clusters, np.mean(locations[:, 0]))

        # Return the dataset requested and the cluster centers for that dataset
        return self.current_results, clusters
    
    def get_crime_types(self):
        results = []

        query = '''
            SELECT DISTINCT primary_type from crimes 
            WHERE primary_type NOT IN (
                'NON-CRIMINAL (SUBJECT SPECIFIED)',
                'NON-CRIMINAL',
                'NON - CRIMINAL'
                )
            '''
        
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()
        query_task = cursor.execute(query)
        first = query_task.fetchone()
        while(first is not None):
            results.append(first[0])
            first = query_task.fetchone()

        return results
    
    def lat_lng_to_meters(self, data):
        # Mean latitude for the dataset
        mean_lat = np.mean(data[:, 0])

        # Convert latitude to meters (1 degree latitude = approx 111 km)
        lat_in_meters = data[:, 0] * 111

        # Convert longitude to meters (1 degree longitude = 111 km * cos(latitude))
        lng_in_meters = data[:, 1] * 111 * np.cos(np.radians(mean_lat))

        return np.column_stack((lat_in_meters, lng_in_meters))

    def meters_to_lat_lng(self, data, reference_latitude):
        # Convert latitude from meters back to degrees
        lat = data[:, 0] / 111

        # Convert longitude from meters back to degrees
        # Need to divide by the cosine of the reference latitude
        lng = data[:, 1] / (111 * np.cos(np.radians(reference_latitude)))

        return np.column_stack((lat, lng))
    
if __name__ == '__main__':
    crimes_test = ChicagoCrimes('./crimes.db')
    print(crimes_test.get_crime_types())