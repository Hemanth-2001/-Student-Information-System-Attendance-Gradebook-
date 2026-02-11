from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from ..models.student import Gender, BloodGroup


class StudentBase(BaseModel):
    admission_number: str = Field(..., max_length=50)
    roll_number: Optional[str] = Field(None, max_length=50)
    date_of_birth: date
    gender: Gender
    blood_group: Optional[BloodGroup] = None
    nationality: str = Field(default="Indian", max_length=100)
    religion: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    
    # Address
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=10)
    country: str = Field(default="India", max_length=100)
    
    # Medical
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contacts: Optional[List[Dict[str, Any]]] = None
    
    # Academic
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    admission_date: date
    previous_school: Optional[str] = Field(None, max_length=255)
    status: str = Field(default="active", max_length=20)


class StudentCreate(StudentBase):
    # User information for creating the user account
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None


class StudentUpdate(BaseModel):
    roll_number: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    religion: Optional[str] = None
    category: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contacts: Optional[List[Dict[str, Any]]] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    status: Optional[str] = None


class StudentResponse(StudentBase):
    id: int
    user_id: int
    
    # Nested user info
    user: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    id: int
    user_id: int
    admission_number: str
    roll_number: Optional[str]
    first_name: str
    last_name: str
    email: str
    class_name: Optional[str] = None
    section_name: Optional[str] = None
    status: str
    
    class Config:
        from_attributes = True


class StudentDetailResponse(StudentResponse):
    # Additional details
    attendance_percentage: Optional[float] = None
    total_attendance_days: Optional[int] = None
    present_days: Optional[int] = None
    
    class Config:
        from_attributes = True
