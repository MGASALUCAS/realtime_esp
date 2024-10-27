import sqlite3
import random
import time

# Function to create the table if it doesn't exist
def create_table():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            trigger TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert dummy data into the SQLite database
def insert_dummy_data(n=40):
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Create a list of possible trigger events
    trigger_events = ['Manual', 'Auto', 'High Temp', 'Low Humidity']

    for _ in range(n):
        # Generate random temperature (between 20 and 40 degrees Celsius)
        temperature = round(random.uniform(20, 40), 2)

        # Generate random humidity (between 30% and 90%)
        humidity = round(random.uniform(30, 90), 2)

        # Randomly select a trigger event
        trigger = random.choice(trigger_events)

        # Generate a random timestamp (last 24 hours)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(0, 86400)))

        # Insert the dummy data into the database
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, temperature, humidity, trigger)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, temperature, humidity, trigger))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()  # Create the table before inserting data
    insert_dummy_data(n=50)  # Insert 50 dummy records into the database
