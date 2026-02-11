from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum as SQLEnum, DateTime, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class AssessmentType(str, enum.Enum):
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    TEST = "test"
    MID_TERM = "mid_term"
    FINAL_EXAM = "final_exam"
    PROJECT = "project"
    PRACTICAL = "practical"
    PRESENTATION = "presentation"
    HOMEWORK = "homework"


class GradeScale(str, enum.Enum):
    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C_PLUS = "C+"
    C = "C"
    D = "D"
    F = "F"


class Assessment(Base):
    """Assignments, tests, quizzes, exams"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    assessment_type = Column(SQLEnum(AssessmentType), nullable=False)
    total_marks = Column(Float, nullable=False)
    passing_marks = Column(Float, nullable=True)
    weightage = Column(Float, default=1.0)  # For weighted grading
    
    date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    is_published = Column(Boolean, default=False)
    instructions = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    grades = relationship("Grade", back_populates="assessment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Assessment {self.title} ({self.assessment_type})>"


class Grade(Base):
    """Individual student grades for assessments"""
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    marks_obtained = Column(Float, nullable=True)
    grade = Column(SQLEnum(GradeScale), nullable=True)
    percentage = Column(Float, nullable=True)
    
    is_absent = Column(Boolean, default=False)
    remarks = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    
    submitted_on = Column(DateTime(timezone=True), nullable=True)
    graded_on = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    assessment = relationship("Assessment", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
    teacher = relationship("Teacher", back_populates="grades")
    
    def __repr__(self):
        return f"<Grade student={self.student_id} assessment={self.assessment_id} marks={self.marks_obtained}>"


class ReportCard(Base):
    """Term/semester report cards"""
    __tablename__ = "report_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    
    term = Column(String(50), nullable=False)  # Term 1, Semester 1, etc.
    
    total_marks = Column(Float, nullable=True)
    marks_obtained = Column(Float, nullable=True)
    percentage = Column(Float, nullable=True)
    grade = Column(String(10), nullable=True)
    rank = Column(Integer, nullable=True)
    
    attendance_percentage = Column(Float, nullable=True)
    total_days = Column(Integer, nullable=True)
    present_days = Column(Integer, nullable=True)
    
    conduct_grade = Column(String(50), nullable=True)
    teacher_remarks = Column(Text, nullable=True)
    principal_remarks = Column(Text, nullable=True)
    
    is_published = Column(Boolean, default=False)
    published_date = Column(Date, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ReportCard student={self.student_id} term={self.term}>"
