import sqlite3
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''
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

init_db()

@app.route('/post_data', methods=['POST'])
def post_data():
    try:
        # Get JSON data from request
        data = request.json

        # Extract values with proper checks
        value1 = data.get('value1')  # Temperature
        value2 = data.get('value2')  # Humidity
        value3 = data.get('value3')  # Trigger event

        # Check if any value is None or empty
        if value1 is None or value2 is None or value3 is None:
            return jsonify({"status": "error", "message": "Missing one or more required fields"}), 400

        # Convert the values to the correct types
        temperature = float(value1)  # Convert to float
        humidity = float(value2)      # Convert to float
        trigger = str(value3)   # Ensure it's a string


        # Insert data into the database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sensor_data (timestamp, temperature, humidity, trigger) VALUES (?, ?, ?, ?)',
                       (datetime.now(), temperature, humidity, trigger))
        conn.commit()

        return jsonify({"status": "success", "message": "Data received and stored successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Dashboard route to display sensor data
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('SELECT timestamp, temperature, humidity, trigger FROM sensor_data ORDER BY timestamp DESC LIMIT 10')
    data = c.fetchall()
    conn.close()
    return render_template('dashboard.html', data=data)

# Toggle relay endpoint
@app.route('/toggle-relay', methods=['POST', 'GET'])
def toggle_relay():
    relay_status = request.args.get('relay_status', 'off')
    message = "ZONE 01 & ZONE 02 FIRE DETECTED AT MSC ROOM" if relay_status == 'on' else "Relay is currently OFF"
    return jsonify({'relay_status': relay_status, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)
