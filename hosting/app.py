from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Function to create/connect to the SQLite database and create the Sensor table
def init_db():
    conn = sqlite3.connect('esp_sensors.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value1 TEXT,
            value2 TEXT,
            value3 TEXT,
            reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Route to fetch the sensor data for visualization
@app.route('/')
def index():
    return render_template('index.html')

# API route to retrieve the latest sensor data (for Highcharts)
@app.route('/api/sensor_data', methods=['GET'])
def sensor_data():
    conn = sqlite3.connect('esp_sensors.db')
    cursor = conn.cursor()
    cursor.execute('SELECT value1, value2, value3, reading_time FROM Sensor ORDER BY reading_time DESC LIMIT 40')
    rows = cursor.fetchall()
    conn.close()

    # Prepare data for Highcharts
    values1 = [row[0] for row in rows]
    values2 = [row[1] for row in rows]
    values3 = [row[2] for row in rows]
    reading_time = [row[3] for row in rows]

    return jsonify({
        'value1': values1[::-1],
        'value2': values2[::-1],
        'value3': values3[::-1],
        'reading_time': reading_time[::-1]
    })

# API route to receive data from the ESP and insert it into the database
@app.route('/api/post_data', methods=['POST'])
def post_data():
    data = request.json
    value1 = data.get('value1')
    value2 = data.get('value2')
    value3 = data.get('value3')
    
    conn = sqlite3.connect('esp_sensors.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Sensor (value1, value2, value3) VALUES (?, ?, ?)
    ''', (value1, value2, value3))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
