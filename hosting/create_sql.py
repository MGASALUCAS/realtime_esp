import sqlite3
import random
import string
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('esp_sensors.db')
cursor = conn.cursor()

# Create Sensor table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sensor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value1 TEXT,
        value2 TEXT,
        value3 TEXT,
        reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Generate random dummy data for the table
def random_value():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# Insert dummy data into the Sensor table
def insert_dummy_data(num_rows):
    for _ in range(num_rows):
        value1 = random_value()
        value2 = random_value()
        value3 = random_value()
        cursor.execute('''
            INSERT INTO Sensor (value1, value2, value3)
            VALUES (?, ?, ?)
        ''', (value1, value2, value3))
    conn.commit()

# Print the chat-like sensor data
def print_sensor_data():
    cursor.execute('SELECT * FROM Sensor')
    rows = cursor.fetchall()
    print("Sensor Data Chat:")
    for row in rows:
        print(f"ID: {row[0]} | Value1: {row[1]} | Value2: {row[2]} | Value3: {row[3]} | Time: {row[4]}")

# Insert 10 rows of dummy data
insert_dummy_data(10)

# Display the data
print_sensor_data()

# Close the connection
conn.close()
