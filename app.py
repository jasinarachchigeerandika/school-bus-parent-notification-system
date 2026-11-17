from flask import Flask, render_template, request, jsonify
from notification import send_seat_update_notification, get_recent_notifications

app = Flask(__name__)

# Simulated Database for Buses & Routes
buses_db = {
    "AB-1234": {"driver": "Mr. Perera", "route": "Colombo - Maharagama", "seats": 24},
    "CD-5678": {"driver": "Mr. Silva", "route": "Kandy - Peradeniya", "seats": 12},
    "EF-9012": {"driver": "Mr. Fernando", "route": "Galle - Matara", "seats": 18}
}

# Simulated Users Database for Parent Authentication (නම සමඟ)
USERS_DB = {
    "parent@gmail.com": {"password": "password123", "name": "Parent"},
    "kamal@gmail.com": {"password": "kamal1234", "name": "Kamal Perera"},
    "arandikahansini@gmail.com": {"password": "password123", "name": "Erandika"}
}

@app.route('/')
def index():
    return render_template('index.html')

# Login API Route එක (ආරක්ෂිත සත්‍යාපනය සහ නම යැවීම සඳහා)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # ඊමේල් සහ පාස්වර්ඩ් එක නිවැරදි දැයි පරීක්ෂා කිරීම
    if email in USERS_DB and USERS_DB[email]["password"] == password:
        return jsonify({
            "success": True, 
            "message": "Login Successful!", 
            "name": USERS_DB[email]["name"]
        })
    else:
        return jsonify({"success": False, "message": "Invalid Email or Password!"}), 401

# අලුතින් එකතු කළ Register API Route එක (අලුත් යූසර්වරුන් සේව් කර නම යැවීම සඳහා)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # ඊමේල් ලිපිනය දැනටමත් පද්ධතියේ ඇද්දැයි පරීක්ෂා කිරීම
    if email in USERS_DB:
        return jsonify({"success": False, "message": "Email already registered!"}), 400
    
    # අලුත් යූසර්ව USERS_DB එකට එකතු කිරීම
    USERS_DB[email] = {"password": password, "name": name}
    
    return jsonify({
        "success": True, 
        "message": "Registration Successful!",
        "name": name
    })

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