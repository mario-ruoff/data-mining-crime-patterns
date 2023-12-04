import numpy as np
import sqlite3

from database.cluster_algorithms import KMeans4, DBSCAN

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
    
    def get_crimes(self, k=2, crime_types=None, year=2023, num_crimes=0):
        crime_types_string = ', '.join(f"'{x}'" for x in crime_types)
        record_limter = '' if num_crimes == 0 else 'LIMIT 10000'
        
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()
        query = f'''
            SELECT latitude,longitude, date, primary_type from crimes
            WHERE arrest=1 and primary_type IN ({crime_types_string}) AND location_description='STREET' AND year={year}
            ORDER BY random()
            {record_limter}
            '''
        
        # Get crimes into numpy array
        self.current_results = []
        raw_results = cursor.execute(query)
        result = raw_results.fetchone()

        # Abort appending if no results
        if result is None:
            return self.current_results, None

        # Append results to array
        while(result is not None):
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()
        
        record_array = np.array(self.current_results)
        locations = record_array[:, (0,1)]

        # Abort clustering if not enough results
        if len(locations) < k:
            return self.current_results, None

        #Apply clustering
        kmeans = KMeans4(n_clusters=k)
        clusters, centroids = kmeans.fit(locations)

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
    
if __name__ == '__main__':
    crimes_test = ChicagoCrimes('./crimes.db')
    print(crimes_test.get_crime_types())