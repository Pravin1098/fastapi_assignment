# Calendly Mock API

## Setup

# 1. Clone
git clone https://github.com/Pravin1098/fastapi_assignment.git
cd fastapi_assignment

# 2. Virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# .\venv\Scripts\activate         # Windows

# 3. Install
pip install -r requirements.txt

# 4. Start
uvicorn backend.api.calendly_integration:app --reload


* Check availability  
* Book an appointment
* Cancel a booking and free the slot  

## Appointment Types & Durations

```python
APPOINTMENT_TYPES = {
    "general_consultation": 30,   # minutes
    "follow_up":            15,
    "physical_exam":        45,
    "specialist_consultation": 60
}


1. Get Availability
curl --location 'http://127.0.0.1:5000/api/calendly/availability?date=2025-10-30&appointment_type=follow_up'
respone ==>
{
    "date": "2025-10-30",
    "available_slots": [
        {
            "start_time": "09:00",
            "end_time": "09:15",
            "available": true
        },
        {
            "start_time": "09:15",
            "end_time": "09:30",
            "available": true
        },
    ]
}


2. Book an Appointment
curl --location 'http://127.0.0.1:5000/api/calendly/book' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "appointment_type": "general_consultation",
    "date": "2025-10-30",
    "start_time": "09:00",
    "patient": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0100"
    },
    "reason": "Annual checkup"
  }'
respone ==>
{
    "booking_id": "APPT-3077",
    "status": "confirmed",
    "confirmation_code": "ZH2P70",
    "details": {
        "appointment_type": "general_consultation",
        "date": "2025-10-30",
        "start_time": "09:00",
        "patient": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-555-0100"
        },
        "reason": "Annual checkup"
    }
}


3. Cancel a Booking
curl --location --request POST 'http://127.0.0.1:5000/api/calendly/cancel/?booking_id=APPT-3077' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data ''
respone ==>
{
    "message": "Booking APPT-3077 canceled and slot freed"
}
