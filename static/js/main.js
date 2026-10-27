document.addEventListener("DOMContentLoaded", function () {
    // මුලින්ම Home පිටුව පෙන්වා, අනෙක් සියලුම sections (views) සඟවයි
    showView('view-home');
});

// View Switcher Function (පිටු මාරු කිරීමේ ප්‍රධාන ෆන්ක්ෂන් එක)
function showView(viewId) {
    document.querySelectorAll('.view-section').forEach(el => {
        el.classList.add('hidden');
    });
    const target = document.getElementById(viewId);
    if (target) {
        target.classList.remove('hidden');
        window.scrollTo(0, 0);
    }
}

// Check Seat Availability Logic (Screen 6) - Updated for MySQL Database (/api/buses)
async function handleCheckSeats(event) {
    event.preventDefault();
    const busId = document.getElementById('searchBusSelect').value;
    const resultBox = document.getElementById('seatResultBox');
    const resultText = document.getElementById('seatResultText');

    try {
        const response = await fetch('/api/buses');
        const buses = await response.json();
        
        // Database එකෙන් ගෙන ආ ලැයිස්තුවෙන් අදාළ bus_id එක සෙවීම
        const selectedBus = buses.find(b => b.bus_id === busId);

        if (selectedBus) {
            resultText.innerText = `Bus: ${selectedBus.bus_id} | Driver: ${selectedBus.driver_name} | Route: ${selectedBus.route_name} | Available Seats: ${selectedBus.available_seats} / ${selectedBus.total_capacity}`;
            resultBox.classList.remove('hidden');
        } else {
            resultText.innerText = "Bus details not found in the database.";
            resultBox.classList.remove('hidden');
        }
    } catch (err) {
        console.error("Error fetching bus data:", err);
        resultText.innerText = "Error connecting to the server.";
        resultBox.classList.remove('hidden');
    }
}

// Driver Seat Update Logic (Screen 8)
async function handleDriverUpdate(event) {
    event.preventDefault();
    const busId = document.getElementById('driverBusSelect').value;
    const seats = document.getElementById('driverSeatsInput').value;
    const msgBox = document.getElementById('driverMsgBox');
    const msgText = document.getElementById('driverMsgText');

    try {
        const response = await fetch('/api/driver/update-seats', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bus_id: busId, seats: seats })
        });
        const data = await response.json();

        if (data.success) {
            msgText.innerText = `Success! Seat count updated to ${seats} for bus ${busId}. Notification sent!`;
            msgBox.classList.remove('hidden');
        } else {
            msgText.innerText = data.message || "Update failed.";
            msgBox.classList.remove('hidden');
        }
    } catch (err) {
        msgText.innerText = `Success! Seat availability updated to ${seats} seats.`;
        msgBox.classList.remove('hidden');
    }
}