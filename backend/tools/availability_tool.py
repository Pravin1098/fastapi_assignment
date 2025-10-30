from datetime import datetime, timedelta
from typing import List
from backend.models.schemas import TimeSlot

# Doctor working hours (for mock)
WORKING_HOURS = {
    "start": "09:00",
    "end": "17:00"
}

# Appointment types with durations (minutes)
APPOINTMENT_TYPES = {
    "general_consultation": 30,
    "follow_up": 15,
    "physical_exam": 45,
    "specialist_consultation": 60
}

# Mock existing appointments (simulate already booked slots)
# EXISTING_APPOINTMENTS = [
#     {"date": "2025-10-30", "start_time": "10:00", "end_time": "10:30"},
#     {"date": "2025-10-30", "start_time": "14:00", "end_time": "14:30"},
# ]

EXISTING_APPOINTMENTS = []


def generate_time_slots(date: str, appointment_type: str) -> List[TimeSlot]:
    """
    Compute available slots for the given date and appointment type
    based on doctor's working hours and existing appointments.
    """
    duration = APPOINTMENT_TYPES.get(appointment_type.lower())
    if not duration:
        raise ValueError("Invalid appointment type")

    work_start = datetime.strptime(f"{date} {WORKING_HOURS['start']}", "%Y-%m-%d %H:%M")
    work_end = datetime.strptime(f"{date} {WORKING_HOURS['end']}", "%Y-%m-%d %H:%M")

    slots = []
    current = work_start
    while current + timedelta(minutes=duration) <= work_end:
        start_time = current.strftime("%H:%M")
        end_time = (current + timedelta(minutes=duration)).strftime("%H:%M")

        # Check if this slot conflicts with existing appointments
        overlap = any(
            appt["date"] == date and not (
                end_time <= appt["start_time"] or start_time >= appt["end_time"]
            )
            for appt in EXISTING_APPOINTMENTS
        )

        slots.append(TimeSlot(start_time=start_time, end_time=end_time, available=not overlap))
        current += timedelta(minutes=duration)

    return slots
