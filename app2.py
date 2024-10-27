from flask import Flask, request, jsonify, render_template
import sqlite3
import time

app = Flask(__name__)

# Database setup (SQLite for simplicity)
def init_db():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            trigger TEXT
        )
    ''')
    conn.commit()
    conn.close()

# API to receive data
@app.route('/post-data', methods=['POST'])
def post_data():
    api_key = request.form.get('api_key')
    if api_key == 'tPmAT5Ab3j7F9':  # Match with ESP32 key
        temperature = request.form.get('value1')
        humidity = request.form.get('value2')
        trigger = request.form.get('trigger')

        # Store data in the database
        conn = sqlite3.connect('sensor_data2.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (timestamp, temperature, humidity, trigger)
            VALUES (?, ?, ?, ?)
        ''', (time.strftime('%Y-%m-%d %H:%M:%S'), temperature, humidity, trigger))
        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'invalid API key'}), 403

# Route to visualize the data
@app.route('/')
def index():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, temperature, humidity, trigger FROM sensor_data ORDER BY timestamp DESC')
    data = cursor.fetchall()
    conn.close()
    return render_template('index2.html', data=data)

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=5000)
