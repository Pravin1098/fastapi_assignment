import random, string
from backend.models.schemas import BookingRequest, BookingResponse
from backend.tools.availability_tool import EXISTING_APPOINTMENTS

# def create_booking(data: BookingRequest) -> BookingResponse:
#     """Create a new mock appointment and return confirmation."""
#     booking_id = f"APPT-{random.randint(1000,9999)}"
#     confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

#     # Add booking to mock list (so it’s blocked next time)
#     start = data.start_time
#     duration_map = {
#         "general_consultation": 30,
#         "follow_up": 15,
#         "physical_exam": 45,
#         "specialist_consultation": 60
#     }
#     end = (int(start.split(":")[0]) * 60 + int(start.split(":")[1]) + duration_map[data.appointment_type.lower()])
#     end_time = f"{end // 60:02d}:{end % 60:02d}"

#     EXISTING_APPOINTMENTS.append({"date": data.date, "start_time": start, "end_time": end_time})

#     return BookingResponse(
#         booking_id=booking_id,
#         status="confirmed",
#         confirmation_code=confirmation_code,
#         details=data.dict()
#     )


# booking_tool.py
def create_booking(data: BookingRequest) -> BookingResponse:
    booking_id = f"APPT-{random.randint(1000,9999)}"
    confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    duration_map = {
        "general_consultation": 30, "follow_up": 15,
        "physical_exam": 45, "specialist_consultation": 60
    }
    duration = duration_map[data.appointment_type.lower()]
    h, m = map(int, data.start_time.split(":"))
    total_min = h * 60 + m + duration
    end_time = f"{total_min // 60:02d}:{total_min % 60:02d}"

    EXISTING_APPOINTMENTS.append({
        "date": data.date,
        "start_time": data.start_time,
        "end_time": end_time
    })

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        confirmation_code=confirmation_code,
        details=data.dict()
    )
