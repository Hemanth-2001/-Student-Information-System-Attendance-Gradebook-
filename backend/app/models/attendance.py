from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum as SQLEnum, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    SICK_LEAVE = "sick_leave"
    EXCUSED = "excused"


class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    status = Column(SQLEnum(AttendanceStatus), nullable=False, default=AttendanceStatus.PRESENT)
    
    # Optional fields
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    marked_by = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    marked_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # For period-wise attendance
    period_number = Column(Integer, nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    marked_by_teacher = relationship("Teacher", back_populates="attendance_records")
    
    def __repr__(self):
        return f"<Attendance student={self.student_id} date={self.date} status={self.status}>"


class AttendanceReport(Base):
    """Monthly attendance summary for students"""
    __tablename__ = "attendance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    
    total_days = Column(Integer, default=0)
    present_days = Column(Integer, default=0)
    absent_days = Column(Integer, default=0)
    late_days = Column(Integer, default=0)
    sick_leave_days = Column(Integer, default=0)
    excused_days = Column(Integer, default=0)
    
    attendance_percentage = Column(String(10), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<AttendanceReport student={self.student_id} {self.month}/{self.year}>"
