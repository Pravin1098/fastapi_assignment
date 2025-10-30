from pydantic import BaseModel, EmailStr
from typing import List, Optional

class TimeSlot(BaseModel):
    start_time: str
    end_time: str
    available: bool = True


class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[TimeSlot]


class PatientInfo(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class BookingRequest(BaseModel):
    appointment_type: str
    date: str
    start_time: str
    patient: PatientInfo
    reason: Optional[str] = None


class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: str
    details: dict
