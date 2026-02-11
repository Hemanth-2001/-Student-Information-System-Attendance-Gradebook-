from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base


class AcademicYear(Base):
    __tablename__ = "academic_years"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(String(20), unique=True, nullable=False)  # e.g., "2024-2025"
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10), nullable=False)
    is_current = Column(Boolean, default=False)
    
    # Relationships
    classes = relationship("Class", back_populates="academic_year")
    
    def __repr__(self):
        return f"<AcademicYear {self.year}>"


class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # e.g., "Class 10", "Grade 5"
    level = Column(Integer, nullable=False)  # 1-12
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    class_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    max_students = Column(Integer, default=40)
    
    # Relationships
    academic_year = relationship("AcademicYear", back_populates="classes")
    class_teacher = relationship("Teacher", back_populates="class_teacher_of")
    sections = relationship("Section", back_populates="class_info", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="class_info")
    subjects = relationship("Subject", back_populates="class_info", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Class {self.name}>"


class Section(Base):
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # e.g., "A", "B", "C"
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    max_students = Column(Integer, default=40)
    
    # Relationships
    class_info = relationship("Class", back_populates="sections")
    students = relationship("Student", back_populates="section")
    
    def __repr__(self):
        return f"<Section {self.name}>"


class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    description = Column(String(500), nullable=True)
    credits = Column(Integer, default=1)
    
    # Relationships
    class_info = relationship("Class", back_populates="subjects")
    teachers = relationship("SubjectTeacher", back_populates="subject", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="subject")
    
    def __repr__(self):
        return f"<Subject {self.code}: {self.name}>"


class SubjectTeacher(Base):
    """Junction table for subject-teacher assignment"""
    __tablename__ = "subject_teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    subject = relationship("Subject", back_populates="teachers")
    teacher = relationship("Teacher", back_populates="subjects")
    
    def __repr__(self):
        return f"<SubjectTeacher subject={self.subject_id} teacher={self.teacher_id}>"
