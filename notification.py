import datetime

# Simulated Database Notification Storage (Database එකක් නැතිව පරීක්ෂා කිරීමට)
notifications_db = []

def send_seat_update_notification(bus_id, available_seats, route_name):
   
    message = f"Notice: Bus {bus_id} ({route_name}) has updated available seats to {available_seats}."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    notif_data = {
        "id": len(notifications_db) + 1,
        "bus_id": bus_id,
        "message": message,
        "timestamp": timestamp,
        "type": "SEAT_UPDATE"
    }
    
    # Store notification in memory / DB
    notifications_db.append(notif_data)
    
    print(f"[NOTIFICATION SENT] -> {message}")
    return notif_data

def send_delay_notification(bus_id, delay_minutes, route_name):
    
    message = f"Alert: Bus {bus_id} on route {route_name} is delayed by {delay_minutes} minutes due to traffic."
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    notif_data = {
        "id": len(notifications_db) + 1,
        "bus_id": bus_id,
        "message": message,
        "timestamp": timestamp,
        "type": "DELAY_ALERT"
    }
    
    notifications_db.append(notif_data)
    print(f"[DELAY ALERT SENT] -> {message}")
    return notif_data

def get_recent_notifications():
    
    return sorted(notifications_db, key=lambda x: x['id'], reverse=True)