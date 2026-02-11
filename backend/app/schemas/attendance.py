from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from ..models.attendance import AttendanceStatus


class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: AttendanceStatus
    remarks: Optional[str] = None
    period_number: Optional[int] = None
    subject_id: Optional[int] = None


class AttendanceCreate(AttendanceBase):
    check_in_time: Optional[datetime] = None


class AttendanceBulkCreate(BaseModel):
    """For marking attendance for multiple students at once"""
    date: date
    period_number: Optional[int] = None
    subject_id: Optional[int] = None
    attendance_records: list[dict]  # [{student_id: int, status: str}, ...]


class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None
    remarks: Optional[str] = None
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None


class AttendanceResponse(AttendanceBase):
    id: int
    check_in_time: Optional[datetime]
    check_out_time: Optional[datetime]
    marked_by: Optional[int]
    marked_at: datetime
    
    # Nested data
    student_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class AttendanceReportResponse(BaseModel):
    student_id: int
    student_name: str
    month: int
    year: int
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    sick_leave_days: int
    excused_days: int
    attendance_percentage: str
    
    class Config:
        from_attributes = True


class AttendanceStatsResponse(BaseModel):
    total_students: int
    present: int
    absent: int
    late: int
    sick_leave: int
    excused: int
    half_day: int
    attendance_percentage: float


class StudentAttendanceSummary(BaseModel):
    student_id: int
    student_name: str
    admission_number: str
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    attendance_percentage: float
    
    class Config:
        from_attributes = True


class DateRangeAttendanceRequest(BaseModel):
    start_date: date
    end_date: date
    class_id: Optional[int] = None
    section_id: Optional[int] = None
