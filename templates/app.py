from flask import Flask, render_template, request, jsonify
import mysql.connector
from notification import send_seat_update_notification, get_recent_notifications

app = Flask(__name__)

# Simulated Database for Buses & Routes
buses_db = {
    "AB-1234": {"driver": "Mr. Perera", "route": "Colombo - Maharagama", "seats": 24},
    "CD-5678": {"driver": "Mr. Silva", "route": "Kandy - Peradeniya", "seats": 12},
    "EF-9012": {"driver": "Mr. Fernando", "route": "Galle - Matara", "seats": 18}
}

# XAMPP MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="school_bus_system"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT full_name FROM parents WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            return jsonify({
                "success": True,
                "message": "Login Successful!",
                "name": user["full_name"]
            })
        else:
            return jsonify({"success": False, "message": "Invalid Email or Password!"}), 401

    except mysql.connector.Error as err:
        print("MySQL Login Error:", err)
        return jsonify({"success": False, "message": "Database error during login!"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone', '')
    password = data.get('password')

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT parent_id FROM parents WHERE email = %s", (email,))
        existing = cursor.fetchone()

        if existing:
            return jsonify({"success": False, "message": "Email already registered!"}), 400

        cursor.execute(
            """
            INSERT INTO parents (full_name, email, phone_number, password)
            VALUES (%s, %s, %s, %s)
            """,
            (full_name, email, phone_number, password)
        )
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Registration Successful!",
            "name": full_name
        })

    except mysql.connector.Error as err:
        print("MySQL Register Error:", err)
        return jsonify({"success": False, "message": "Database error during registration!"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/seats/<bus_id>', methods=['GET'])
def get_seats(bus_id):
    bus = buses_db.get(bus_id)
    if bus:
        return jsonify({"success": True, "seats": bus["seats"], "bus": bus})
    return jsonify({"success": False, "message": "Bus not found"}), 404

@app.route('/api/driver/update-seats', methods=['POST'])
def update_seats():
    data = request.json
    bus_id = data.get('bus_id')
    new_seats = data.get('seats')

    if bus_id in buses_db:
        buses_db[bus_id]['seats'] = int(new_seats)
        route = buses_db[bus_id]['route']

        # Trigger notification module helper
        send_seat_update_notification(bus_id, new_seats, route)

        return jsonify({"success": True, "message": "Seats updated successfully!"})

    return jsonify({"success": False, "message": "Invalid Bus ID"}), 400

@app.route('/api/notifications', methods=['GET'])
def fetch_notifications():
    return jsonify({"success": True, "notifications": get_recent_notifications()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)