import sqlite3
import pandas as pd

connection = sqlite3.connect('energy_efficiency_and_wealth.db') # create a new database and connect to it
cursor = connection.cursor() # create a cursor object we can use to interact with our database connection

# import data!
ll84_df = pd.read_pickle('../data/clean/ll84_cleaned.pkl')
acs_df = pd.read_pickle('../data/clean/acs_cleaned.pkl')

# write dataframes to SQL db