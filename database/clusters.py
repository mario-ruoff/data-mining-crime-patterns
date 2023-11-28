import numpy as np
import os
import sqlite3

from sklearn.cluster import KMeans

class ChicagoCrimes:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.current_results = []
        self.num_clusters = 0

        # add logic here to preprocess the database
        # here we should try to go through the crimes
        # database in order to figure out outliers,
        # this will help with clustering later
        
    def get_police_stations(self):

        # something something database
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()

        query = '''
            SELECT latitude,longitude from police
            LIMIT 100
            '''
        
        self.current_results = []
        raw_results = cursor.execute(query)
        result = raw_results.fetchone()
        while(result is not None):
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()

        self.num_clusters = len(self.current_results)
        return self.current_results
    
    def get_crimes(self, k=2, crime_types=None, year=None):
        crime_types_string = ', '.join(f"'{x}'" for x in crime_types)
        
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()
        query = f'''
            SELECT latitude,longitude, date, primary_type from crimes
            WHERE arrest=0 and primary_type IN ({crime_types_string}) AND location_description='STREET' AND year={year}
            ORDER BY date
            LIMIT 10000
            '''
        
        self.current_results = []
        raw_results = cursor.execute(query)
        result = raw_results.fetchone()
        if result is None:
            return self.current_results, None

        while(result is not None):
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()
        
        record_array = np.array(self.current_results)
        locations = record_array[:, (0,1)]

        k = KMeans(n_clusters=k, n_init='auto')
        k.fit(locations)
        clusters = k.cluster_centers_

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