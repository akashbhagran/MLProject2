import pandas as pd
import sqlite3

conn = sqlite3.connect('C:/Users/akash/Documents/MLProjects/LiveData/fruits.db')
df = pd.read_sql("SELECT * FROM FRUITS", conn)
conn.close()

if __name__ == '__main__':
    print(df[['MASS', 'WIDTH','HEIGHT']])
