import numpy as np
import sqlite3 as sql
import time
import redis
import os

redis_host = os.getenv('REDIS_HOST')
r = redis.Redis(host = redis_host)

conn = sql.connect('data/fruits.db')

cursor = conn.cursor()

# Create the FRUITS table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS FRUITS
                 (MASS FLOAT NOT NULL,
                  WIDTH FLOAT NOT NULL,
                  HEIGHT FLOAT NOT NULL,
                  COLOUR FLOAT NOT NULL,
                  FRUIT TEXT NOT NULL,
                  FRUITLABEL TEXT NOT NULL);''')

# Connect to the database

# Function to insert fruit data into the database
def insert_fruit(mass, width, height, colour, fruit, label):
    cursor.execute("INSERT INTO FRUITS (MASS, WIDTH, HEIGHT, COLOUR, FRUIT, FRUITLABEL) VALUES (?, ?, ?, ?, ?,?)",
                   (mass, width, height, colour, fruit, label))

# Function to retrieve the oldest fruit from the database
def get_oldest_fruit():
    cursor.execute("SELECT * FROM FRUITS ORDER BY ROWID ASC LIMIT 1")
    return cursor.fetchone()

# Function to delete the oldest fruit from the database
def delete_oldest_fruit():
    cursor.execute("DELETE FROM FRUITS WHERE ROWID IN (SELECT ROWID FROM FRUITS ORDER BY ROWID ASC LIMIT 1)")

# Function to create a new fruit and manage FIFO
def make_fruit():

    r = np.random.randint(1, 5)

    if get_fruit_count() >= 3000:
        delete_oldest_fruit()

    if r == 1:
        apple_mass = np.random.normal(165, 10)
        apple_width = np.random.normal(7.6, 0.8)
        apple_height = np.random.normal(7.2, 0.6)
        apple_colour = np.random.uniform(0.55, 0.95)
        insert_fruit(apple_mass, apple_width, apple_height, apple_colour, 'apple', 1)
    elif r == 2:
        mandarin_mass = np.random.normal(81, 5)
        mandarin_width = np.random.uniform(5.8, 6.2)
        mandarin_height = np.random.normal(4.3, 0.5)
        mandarin_colour = np.random.uniform(0.77, 0.81)
        insert_fruit(mandarin_mass, mandarin_width, mandarin_height, mandarin_colour, 'mandarin', 2)
    elif r == 3:
        orange_mass = np.random.normal(180, 50)
        orange_width = np.random.normal(7.2, 0.8)
        orange_height = np.random.normal(7.0, 10)
        orange_colour = np.random.uniform(0.72, 0.82)
        insert_fruit(orange_mass, orange_width, orange_height, orange_colour, 'orange', 3)
    elif r == 4:
        lemon_mass = np.random.uniform(50, 200)
        lemon_width = np.random.normal(6.6, 0.6)
        lemon_height = np.random.uniform(7.5, 10.5)
        lemon_colour = np.random.normal(0.72, 0.82)
        insert_fruit(lemon_mass, lemon_width, lemon_height, lemon_colour, 'lemon', 4)

# Function to get the count of fruits in the database
def get_fruit_count():
    cursor.execute("SELECT COUNT(*) FROM FRUITS")
    return cursor.fetchone()[0]

# Continuously insert fruits into the database

if __name__ == '__main__':

    for i in range(0,1000):

        make_fruit()

    while True:
        
        make_fruit()
        conn.commit()

        time.sleep(5)

    # Close the connection
    #conn.close()