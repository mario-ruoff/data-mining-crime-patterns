import os
import sqlite3

class ChicagoCrimes:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.current_results = []
        
    def update_results(self, sql_query):
        # something something database
        db_connection = sqlite3.connect(self.db_file)
        cursor = db_connection.cursor()

        query = '''
            SELECT * from crimes
            LIMIT 100
            '''

        return [
            (41.8982, -87.6097),
            (41.9382, -87.6397),
            (41.9082, -87.7797),
            (41.7682, -87.6397),
            (41.8482, -87.6497),
        ]