import os
import sqlite3

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
            print(result)
            self.current_results.append((result[0], result[1]))
            result = raw_results.fetchone()

        return self.current_results
    
    def get_crimes(self, sql_query=None):

            # something something database
            db_connection = sqlite3.connect(self.db_file)
            cursor = db_connection.cursor()

            query = '''
                SELECT latitude,longitude from crimes
                ORDER BY RANDOM()
                LIMIT 1000
                '''
            
            self.current_results = []
            raw_results = cursor.execute(query)
            result = raw_results.fetchone()
            while(result is not None):
                print(result)
                self.current_results.append((result[0], result[1]))
                result = raw_results.fetchone()

            return self.current_results
