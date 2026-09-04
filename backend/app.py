from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI(
    title="PULSE IoT Smart Ambulance API",
    description="Backend API for IoT Smart Ambulance System",
    version="1.0"
)

# =========================================================
# DATA STORAGE
# =========================================================

sos_history = []

# Emergency contacts
emergency_contacts = []

# Hospital notifications
hospital_notifications = []

# User accounts
users = []


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "PULSE Smart Ambulance Backend is Running",
        "status": "online"
    }

# =========================================================
# USER SIGN UP
# =========================================================

@app.post("/api/signup")
def signup_user(data: dict = Body(...)):

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check required fields
    if not username or not email or not password:

        return {
            "status": "ERROR",
            "message": "Username, email and password are required"
        }

    # Check if email already exists
    for user in users:

        if user["email"] == email:

            return {
                "status": "ERROR",
                "message": "Email already registered"
            }

    # Create new user
    user = {

        "id": len(users) + 1,

        "username": username,

        "email": email,

        "password": password
    }

    # Save user
    users.append(user)

    return {

        "status": "SUCCESS",

        "message":
            "Account created successfully",

        "user": {

            "id": user["id"],

            "username": user["username"],

            "email": user["email"]
        }
    }

# =========================================================
# USER LOGIN
# =========================================================

@app.post("/api/login")
def login_user(data: dict = Body(...)):

    email = data.get("email")
    password = data.get("password")

    # Check required fields
    if not email or not password:

        return {
            "status": "ERROR",
            "message": "Email and password are required"
        }

    # Check user
    for user in users:

        if (
            user["email"] == email
            and user["password"] == password
        ):

            return {

                "status": "SUCCESS",

                "message":
                    "Login successful",

                "user": {

                    "id": user["id"],

                    "username":
                        user["username"],

                    "email":
                        user["email"]
                }
            }

    # Invalid login
    return {

        "status": "ERROR",

        "message":
            "Invalid email or password"
    }


# =========================================================
# LIVE VITALS
# =========================================================

@app.get("/api/vitals")
def get_vitals():

    heart_rate = random.randint(110, 125)
    spo2 = random.randint(96, 99)
    speed = random.randint(55, 70)

    return {
        "heart_rate": heart_rate,
        "spo2": spo2,
        "speed": speed,
        "timestamp": datetime.now().isoformat()
    }


# =========================================================
# GPS LOCATION
# =========================================================

@app.get("/api/location")
def get_location():

    return {
        "latitude": 19.0760 + random.uniform(-0.001, 0.001),
        "longitude": 72.8777 + random.uniform(-0.001, 0.001),
        "timestamp": datetime.now().isoformat()
    }


# =========================================================
# AMBULANCE STATUS
# =========================================================

@app.get("/api/ambulance")
def ambulance_status():

    return {
        "ambulance_id": "MH-12-AMB-0417",
        "status": "EN ROUTE",
        "priority": 1,
        "eta": "04:32",
        "route": "Route 4",
        "hospital": "City Hospital"
    }


# =========================================================
# EMERGENCY CONTACT - ADD
# =========================================================

@app.post("/api/emergency-contacts")
def add_emergency_contact(data: dict = Body(...)):

    name = data.get("name")
    phone = data.get("phone")

    if not name or not phone:

        return {
            "status": "ERROR",
            "message": "Name and phone number are required"
        }

    contact = {
        "id": len(emergency_contacts) + 1,
        "name": name,
        "phone": phone
    }

    emergency_contacts.append(contact)

    return {
        "status": "CONTACT SAVED",
        "message": "Emergency contact saved successfully",
        "contact": contact
    }


# =========================================================
# GET ALL EMERGENCY CONTACTS
# =========================================================

@app.get("/api/emergency-contacts")
def get_emergency_contacts():

    return {
        "total_contacts": len(emergency_contacts),
        "contacts": emergency_contacts
    }


# =========================================================
# DELETE EMERGENCY CONTACT
# =========================================================

@app.delete("/api/emergency-contacts/{contact_id}")
def delete_emergency_contact(contact_id: int):

    for contact in emergency_contacts:

        if contact["id"] == contact_id:

            emergency_contacts.remove(contact)

            return {
                "status": "DELETED",
                "message": "Emergency contact deleted successfully"
            }

    return {
        "status": "ERROR",
        "message": "Contact not found"
    }


# =========================================================
# SOS
# =========================================================

@app.post("/api/sos")
def emergency_sos(data: dict = Body(...)):

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Contacts received from frontend
    contacts = data.get("contacts", [])

    # Google Maps link
    map_link = None

    if latitude is not None and longitude is not None:

        map_link = (
            f"https://www.google.com/maps?q="
            f"{latitude},{longitude}"
        )

    # -----------------------------------------------------
    # SOS DATA
    # -----------------------------------------------------

    sos_data = {

        "id": len(sos_history) + 1,

        "status": "SOS ACTIVATED",

        "message":
            "Emergency alert sent to control room",

        "ambulance_id":
            "MH-12-AMB-0417",

        "latitude":
            latitude,

        "longitude":
            longitude,

        "map_link":
            map_link,

        "contacts_notified":
            len(contacts),

        "timestamp":
            datetime.now().isoformat()
    }

    # Save SOS history
    sos_history.append(sos_data)


    # -----------------------------------------------------
    # EMERGENCY CONTACT ALERT
    # -----------------------------------------------------

    contact_alerts = []

    for contact in contacts:

        alert = {

            "name":
                contact.get("name"),

            "phone":
                contact.get("phone"),

            "message":
                "🚨 EMERGENCY! SOS activated. "
                "Please contact the person immediately.",

            "location":
                map_link,

            "timestamp":
                datetime.now().isoformat()
        }

        contact_alerts.append(alert)


    # -----------------------------------------------------
    # HOSPITAL NOTIFICATION
    # -----------------------------------------------------
   
    hospital_notification = {

        
        "id": len(hospital_notifications) + 1,

        "hospital":
            "City Hospital",

        "status":
            "EMERGENCY NOTIFICATION GENERATED",

        "ambulance_id":
            "MH-12-AMB-0417",

        "latitude":
            latitude,

        "longitude":
            longitude,

        "map_link":
            map_link,

        "message":
            "🚨 Emergency SOS received. "
            "Ambulance assistance required.",

        "timestamp":
            datetime.now().isoformat()
    }

    hospital_notifications.append(
        hospital_notification
    )


    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return {

        **sos_data,

        "emergency_contact_alerts":
            contact_alerts,

        "hospital_notification":
            hospital_notification
    }


# =========================================================
# SOS HISTORY
# =========================================================

@app.get("/api/sos-history")
def get_sos_history():

    return {

        "total_sos":
            len(sos_history),

        "history":
            sos_history
    }


# =========================================================
# EMERGENCY CONTACT ALERT
# =========================================================

@app.post("/api/emergency-alert")
def emergency_alert(data: dict = Body(...)):

    phone = data.get("phone")
    message = data.get("message")

    return {

        "status":
            "ALERT GENERATED",

        "phone":
            phone,

        "message":
            message,

        "timestamp":
            datetime.now().isoformat()
    }


# =========================================================
# HOSPITAL NOTIFICATIONS
# =========================================================

@app.get("/api/hospital-notifications")
def get_hospital_notifications():

    return {

        "total_notifications":
            len(hospital_notifications),

        "notifications":
            hospital_notifications
    }

# =========================================================
# HOSPITAL ACKNOWLEDGE ALERT
# =========================================================

@app.post("/api/hospital-notifications/{notification_id}/acknowledge")
def acknowledge_hospital_notification(notification_id: int):

    for notification in hospital_notifications:

        # Give each notification an ID if it doesn't already have one
        if "id" not in notification:
            notification["id"] = (
                hospital_notifications.index(notification) + 1
            )

        if notification["id"] == notification_id:

            notification["status"] = "ACKNOWLEDGED"

            notification["acknowledged_at"] = (
                datetime.now().isoformat()
            )

            return {
                "status": "SUCCESS",
                "message": "Hospital acknowledged the emergency alert",
                "notification": notification
            }

    return {
        "status": "ERROR",
        "message": "Hospital notification not found"
    }

# -----------------------------
# HOSPITAL BED AVAILABILITY
# -----------------------------
@app.get("/api/hospital-beds")
def hospital_beds():

    return {
        "hospital": "City Hospital",
        "total_beds": 100,
        "available_beds": 24,
        "occupied_beds": 76,
        "icu_total": 20,
        "icu_available": 5,
        "last_updated": datetime.now().isoformat()
    }