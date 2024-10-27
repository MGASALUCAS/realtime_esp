from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Mock data for sensor readings
data = [
    # # Sample data with timestamps, temperature, humidity, and event trigger
    ["2024-10-20 10:00", "25.5", "60", "Normal"],
    ["2024-10-20 10:05", "26.0", "62", "Normal"],
    ["2024-10-20 10:00", "25.5", "60", "Normal"],
    ["2024-10-20 10:05", "26.0", "62", "Normal"],
    ["2024-10-20 10:00", "25.5", "60", "Normal"],
    ["2024-10-20 10:05", "26.0", "62", "Normal"],
    ["2024-10-20 10:00", "25.5", "60", "Normal"],
    ["2024-10-20 10:05", "26.0", "62", "Normal"],
    # # Add more rows as needed
]

# Relay status flag
relay_status = False

@app.route('/')
def index():
    return render_template('index3.html', data=data)

@app.route('/toggle-relay', methods=['POST', 'GET'])
def toggle_relay():
    global relay_status
    relay_status = not relay_status

    # Send different status messages based on flags
    message = ""
    if relay_status:
        message = "ZONE 01 & ZONE 02 FIRE DETECTED AT MSC ROOM"
    else:
        message = "Relay is OFF"

    # Sample flags and messages
    relay_flag = relay_status
    accesskey_status = True  # Mocked status
    fire_flag = False  # Mocked fire detection flag
    release_initiated_flag = False  # Mocked release flag
    hold_active_flag = False  # Mocked hold flag

    if relay_flag:
        message = "RELAY IS ON"
    else:
        message = "RELAY IS OFF"

    if accesskey_status:
        message += " | GCU is in Auto & Manual mode Status 1"
    else:
        message += " | GCU is in Manual mode Status 0"

    if fire_flag:
        message += " | ZONE 01 & ZONE 02 FIRE DETECTED AT MSC ROOM"
    else:
        message += " | MSC ROOM IS NORMAL"

    if release_initiated_flag:
        message += " | FIRE DETECTED AT MSC ROOM, CYLINDER HAS ONLY 60SEC BEFORE DISCHARGING"
    else:
        message += " | RELEASE INITIATED NORMAL_OKAY"

    if hold_active_flag:
        message += " | PANEL IS IN HOLD MODE BEFORE THE CYLINDER DISCHARGE"
    else:
        message += " | HOLD MODE NORMAL_OKAY"

    # Send the status message and relay state
    return jsonify({'relay_status': 'on' if relay_status else 'off', 'message': message})

if __name__ == '__main__':
    app.run(debug=True)
