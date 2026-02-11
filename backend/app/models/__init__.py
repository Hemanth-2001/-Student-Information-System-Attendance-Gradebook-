# Import all models here for Alembic auto-detection
from .user import User, UserRole
from .student import Student, Gender, BloodGroup
from .teacher import Teacher, Parent, ParentStudent
from .academic import AcademicYear, Class, Section, Subject, SubjectTeacher
from .attendance import Attendance, AttendanceStatus, AttendanceReport
from .gradebook import Assessment, Grade, ReportCard, AssessmentType, GradeScale

__all__ = [
    "User",
    "UserRole",
    "Student",
    "Gender",
    "BloodGroup",
    "Teacher",
    "Parent",
    "ParentStudent",
    "AcademicYear",
    "Class",
    "Section",
    "Subject",
    "SubjectTeacher",
    "Attendance",
    "AttendanceStatus",
    "AttendanceReport",
    "Assessment",
    "Grade",
    "ReportCard",
    "AssessmentType",
    "GradeScale",
]
