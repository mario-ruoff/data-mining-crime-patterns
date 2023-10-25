import matplotlib.pyplot as plt
import numpy as np
import os
import sqlite3

from sklearn.cluster import KMeans


# PARAMETERS
DB_FILE = './crimes.db'
DB_FILE_FULL = '/home/zak/Code/data-mining-group-4/database/crimes.db'
SQL_SCRIPT = './queries.sql'
DEBUG_TOGGLE = True

# CONSTANTS
DATETIME_FORMAT = "%m/%d/%Y %I:%M:%S %p"

# Database import
records = []
db_connection = sqlite3.connect(DB_FILE_FULL)
cursor = db_connection.cursor()

if DEBUG_TOGGLE:
    print("Database connection successful...")

# Get the appropriate records from the database, based on the query
query_string = '''
                SELECT latitude,longitude, date, primary_type from crimes
                WHERE arrest=0 and primary_type='ASSAULT' and year=2023
                ORDER BY date
                LIMIT 100
                '''

results = cursor.execute(query_string)
result = results.fetchone()
while(result is not None):
    records.append(result)
    result = results.fetchone()
    print(result)

print(str(len(records)))

# Use K-Means Clustering to cluster the results in a graph

# Get the number of clusters from the number of police stations:
query_string = '''
        SELECT latitude,longitude from police
        '''
cursor.execute(query_string)
n_clusters = len(cursor.fetchall())


record_array = np.array(records)
locations = record_array[:, (0,1)]
inertias = []
k = None

for i in range(1, n_clusters):
    k = KMeans(n_clusters=i, n_init='auto')
    k.fit(locations)
    inertias.append(k.inertia_)
    print(f'##### Cluster {i} #####')
    print(k.cluster_centers_)
    print(f'#####')

plt.scatter(locations[0], locations[1])
#plt.show()

plt.plot(range(1,n_clusters), inertias, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()