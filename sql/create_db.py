import sqlite3
import pandas as pd

conn = sqlite3.connect('energy_efficiency_and_wealth.db') # create a new database and connect to it
cursor = conn.cursor() # create a cursor object we can use to interact with our database connection

# import data!
ll84_df = pd.read_pickle('../data/clean/ll84_cleaned.pkl')
acs_df = pd.read_pickle('../data/clean/acs_cleaned.pkl')
pluto_df = pd.read_pickle('../data/clean/pluto_cleaned.pkl')

# write dataframes to SQL db
# to_sql a pandas method which handles CREATE TABLE and INSERT statements
ll84_df.to_sql('ll84', conn, if_exists='replace', index=False) # index false leaves out pandas auto row index
acs_df.to_sql('acs', conn, if_exists='replace', index=False)
pluto_df.to_sql('pluto', conn, if_exists='replace', index=False)

print("Tables written successfully")
print(f"ll84: {len(ll84_df)} rows")
print(f"acs: {len(acs_df)} rows")
print(f"pluto: {len(pluto_df)} rows")

query = """
    SELECT 
        p.county,
        p.tract,
        a.income,
        AVG(l.eui) as avg_eui,
        COUNT(l.bbl) as building_count
    FROM ll84 l
    JOIN pluto p ON l.bbl = p.bbl
    JOIN acs a ON p.county = a.county AND p.tract = a.tract
    GROUP BY p.county, p.tract, a.income
    ORDER BY a.income DESC
"""
# p, l, a shorthand for data tables
# join all the data together, then group it by census tract (ll84 eui data is more granular down to building level, redundant info)
# income in group by since it doesn't have single val per row
# AVG averages within groups
# select says present these values as new columns

result_df = pd.read_sql_query(query, conn)
conn.close()

print(f"Tracts returned: {len(result_df)}")
print(result_df.head(10))