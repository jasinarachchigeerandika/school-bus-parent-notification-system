import datetime

# In-memory notification storage list
notifications_db = [
    {"id": 1, "bus_id": "CD-5678", "message": "Bus CD-5678 is delayed by 10 minutes due to traffic.", "timestamp": "10 mins ago"}
]

def send_seat_update_notification(bus_id, available_seats, route_name):
    message = f"Notice: Bus {bus_id} ({route_name}) has updated available seats to {available_seats}."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    notif_data = {
        "id": len(notifications_db) + 1,
        "bus_id": bus_id,
        "message": message,
        "timestamp": timestamp
    }
    
    notifications_db.append(notif_data)
    print(f"[NOTIFICATION] {message}")
    return notif_data

def get_recent_notifications():
    return sorted(notifications_db, key=lambda x: x['id'], reverse=True)
