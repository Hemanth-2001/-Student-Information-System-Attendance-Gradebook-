from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text
from sqlalchemy.orm import relationship
from ..core.database import Base


class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Professional Information
    qualification = Column(String(255), nullable=True)
    specialization = Column(String(255), nullable=True)
    experience_years = Column(Integer, default=0)
    joining_date = Column(Date, nullable=False)
    
    # Contact Information
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    
    # Emergency Contact
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    
    # Status
    is_class_teacher = Column(Boolean, default=False)
    status = Column(String(20), default="active")  # active, on_leave, resigned
    
    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    subjects = relationship("SubjectTeacher", back_populates="teacher", cascade="all, delete-orphan")
    class_teacher_of = relationship("Class", back_populates="class_teacher")
    attendance_records = relationship("Attendance", back_populates="marked_by_teacher")
    grades = relationship("Grade", back_populates="teacher")
    
    def __repr__(self):
        return f"<Teacher {self.employee_id}>"


class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Personal Information
    occupation = Column(String(255), nullable=True)
    annual_income = Column(String(50), nullable=True)
    
    # Address Information
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="parent_profile")
    children = relationship("ParentStudent", back_populates="parent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Parent {self.user_id}>"


class ParentStudent(Base):
    """Junction table for parent-student relationship"""
    __tablename__ = "parent_students"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    relation = Column(String(50), nullable=False)  # father, mother, guardian
    is_primary_contact = Column(Boolean, default=False)
    
    # Relationships
    parent = relationship("Parent", back_populates="children")
    student = relationship("Student", back_populates="parent_students")
    
    def __repr__(self):
        return f"<ParentStudent parent={self.parent_id} student={self.student_id}>"
