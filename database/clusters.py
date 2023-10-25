import numpy as np
import os
import sqlite3

from sklearn.cluster import KMeans

class ChicagoCrimes:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.current_results = []
        
    def get_police_stations(self, sql_query=None):

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

        return self.current_results
    
    def get_crimes(self, sql_query=None):

        # something something database
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()

        query = '''
            SELECT latitude,longitude, date, primary_type from crimes
            WHERE arrest=0 and primary_type='ASSAULT' and year=2023
            ORDER BY date
            LIMIT 1000000
            '''
        
        self.current_results = []
        raw_results = cursor.execute(query)
        result = raw_results.fetchone()

        while(result is not None):
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()

        record_array = np.array(self.current_results)
        locations = record_array[:, (0,1)]

        k = KMeans(n_clusters=20, n_init='auto')
        k.fit(locations)
        clusters = k.cluster_centers_

        return self.current_results, clusters