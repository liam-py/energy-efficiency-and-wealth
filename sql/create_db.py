import sqlite3
import pandas as pd

connection = sqlite3.connect('energy_efficiency_and_wealth.db')
cursor = connection.cursor()