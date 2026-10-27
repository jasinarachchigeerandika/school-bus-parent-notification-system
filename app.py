from flask import Flask, render_template, request, jsonify
from notification import send_seat_update_notification, get_recent_notifications

app = Flask(__name__)

# Simulated Database for Buses & Routes
buses_db = {
    "AB-1234": {"driver": "Mr. Perera", "route": "Colombo - Maharagama", "seats": 24},
    "CD-5678": {"driver": "Mr. Silva", "route": "Kandy - Peradeniya", "seats": 12},
    "EF-9012": {"driver": "Mr. Fernando", "route": "Galle - Matara", "seats": 18}
}

@app.route('/')
def index():
    return render_template('index.html')

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