# calendly_integration.py
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from backend.models.schemas import AvailabilityResponse, BookingRequest, BookingResponse
from backend.tools.availability_tool import generate_time_slots, EXISTING_APPOINTMENTS
from backend.tools.booking_tool import create_booking
import uuid

app = FastAPI(title="Mock Calendly API", version="1.0")

# In-memory store for confirmed bookings (for cancellation)
CONFIRMED_BOOKINGS = {}  # {booking_id: BookingResponse dict}


@app.get("/api/calendly/availability", response_model=AvailabilityResponse)
def get_availability(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    appointment_type: str = Query(..., description="Type of appointment")
):
    try:
        slots = generate_time_slots(date, appointment_type)
        return AvailabilityResponse(date=date, available_slots=slots)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/calendly/book", response_model=BookingResponse)
def book_appointment(request: BookingRequest):
    try:
        # Check if slot is still available
        slots = generate_time_slots(request.date, request.appointment_type)
        target_slot = next(
            (s for s in slots if s.start_time == request.start_time and s.available),
            None
        )
        if not target_slot:
            raise HTTPException(status_code=400, detail="Selected time slot is no longer available")

        # Create booking
        response = create_booking(request)
        CONFIRMED_BOOKINGS[response.booking_id] = response.dict()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/calendly/cancel")
def cancel_booking(booking_id: str = Query(..., description="Booking ID to cancel")):
    if booking_id not in CONFIRMED_BOOKINGS:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking = CONFIRMED_BOOKINGS[booking_id]
    details = booking["details"]
    date = details["date"]
    start_time = details["start_time"]

    duration_map = {
        "general_consultation": 30, "follow_up": 15,
        "physical_exam": 45, "specialist_consultation": 60
    }
    duration = duration_map.get(details["appointment_type"].lower(), 30)
    h, m = map(int, start_time.split(":"))
    total_min = h * 60 + m + duration
    end_time = f"{total_min // 60:02d}:{total_min % 60:02d}"

    # Remove exact match
    removed = False
    for appt in EXISTING_APPOINTMENTS[:]:
        if (appt["date"] == date and
            appt["start_time"] == start_time and
            appt["end_time"] == end_time):
            EXISTING_APPOINTMENTS.remove(appt)
            removed = True
            break

    if not removed:
        print(f"[CANCEL FAIL] No match for {date} {start_time}-{end_time}")
        print(f"Current: {EXISTING_APPOINTMENTS}")

    del CONFIRMED_BOOKINGS[booking_id]
    return {"message": f"Booking {booking_id} canceled and slot freed"}