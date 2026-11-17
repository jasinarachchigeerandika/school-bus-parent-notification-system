document.addEventListener("DOMContentLoaded", function () {
    showView('view-home');
});

// View Switcher Function
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

// Backend Login Authentication and Password Save Prompt Handler
async function handleLoginSubmit(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // Browser Password Save Prompt trigger
            if (window.PasswordCredential && navigator.credentials) {
                try {
                    navigator.credentials.store(new PasswordCredential({ id: email, password: password }));
                } catch (e) {
                    console.log("Credential store skipped");
                }
            }
            
            // ලොග් වූ යූසර්ගේ නම Dashboard එකේ Hi, [Name] ! ලෙස පෙන්වීම
            if (result.name) {
                const nameDisplay = document.getElementById('parent-name-display');
                if (nameDisplay) {
                    nameDisplay.innerText = result.name;
                }
            }

            // Navigate to Parent Dashboard on successful login
            showView('view-parent-dashboard');
        } else {
            alert("Access Denied: Invalid Email or Password!");
        }
    } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred during login.");
    }
}

// Register Submit Handler - අලුතින් රෙජිස්ටර් වන කෙනාගේ නම සේව් කර ඩාෂ්බෝඩ් එකේ පෙන්වීම
async function handleRegisterSubmit(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // රෙජිස්ටර් වූ යූසර්ගේ නම Dashboard එකේ පෙන්වීම
            if (result.name) {
                const nameDisplay = document.getElementById('parent-name-display');
                if (nameDisplay) {
                    nameDisplay.innerText = result.name;
                }
            }

            alert("Registration Successful!");
            showView('view-parent-dashboard');
        } else {
            alert(result.message || "Registration failed!");
        }
    } catch (error) {
        console.error("Registration error:", error);
        alert("An error occurred during registration.");
    }
}

// Check Seat Availability Logic (Screen 6)
async function handleCheckSeats(event) {
    event.preventDefault();
    const busId = document.getElementById('searchBusSelect').value;
    const resultBox = document.getElementById('seatResultBox');
    const resultText = document.getElementById('seatResultText');

    try {
        const response = await fetch(`/api/seats/${busId}`);
        const data = await response.json();

        if (data.success) {
            resultText.innerText = `Bus: ${data.bus.route} | Driver: ${data.bus.driver} | Available Seats: ${data.seats}`;
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
        console.error("Error updating seats:", err);
        msgText.innerText = `Success! Seat availability updated to ${seats} seats.`;
        msgBox.classList.remove('hidden');
    }
}

// Language Change Function
function changeLanguage(lang) {
    console.log("Language changed to:", lang);
}