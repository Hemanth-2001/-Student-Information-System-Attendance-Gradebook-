from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class BloodGroup(str, enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    admission_number = Column(String(50), unique=True, index=True, nullable=False)
    roll_number = Column(String(50), nullable=True)
    
    # Personal Information
    date_of_birth = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    blood_group = Column(SQLEnum(BloodGroup), nullable=True)
    nationality = Column(String(100), default="Indian")
    religion = Column(String(100), nullable=True)
    category = Column(String(50), nullable=True)  # General, OBC, SC, ST
    
    # Address Information
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    country = Column(String(100), default="India")
    
    # Medical Information
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    
    # Emergency Contacts
    emergency_contacts = Column(JSON, nullable=True)  # List of contact objects
    
    # Academic Information
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    admission_date = Column(Date, nullable=False)
    previous_school = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(20), default="active")  # active, inactive, graduated, transferred
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    class_info = relationship("Class", back_populates="students")
    section = relationship("Section", back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    parent_students = relationship("ParentStudent", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student {self.admission_number}>"
