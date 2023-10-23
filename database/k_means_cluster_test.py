import sqlite3
import matplotlib.pylab as plt
import numpy as np

from datetime import datetime
from sklearn.cluster import k_means

# PARAMETERS
DB_FILE = './crimes.db'
SQL_SCRIPT = './queries.sql'
DEBUG_TOGGLE = True

# CONSTANTS
DATETIME_FORMAT = "%m/%d/%Y %I:%M:%S %p"

# Database import
records = []
db_connection = sqlite3.connect(DB_FILE)
cursor = db_connection.cursor()

if DEBUG_TOGGLE:
    print("Database connection successful...")

# Get the appropiate records from the database, based on the query
query_string = '''
SELECT * from crimes
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
record_array = np.array(records)
y = record_array[:,3]
x = record_array[:,4]

sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))

fig, ax = plt.subplots()
ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)
plt.show()