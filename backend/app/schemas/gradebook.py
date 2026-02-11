from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from ..models.gradebook import AssessmentType, GradeScale


class AssessmentBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    subject_id: int
    assessment_type: AssessmentType
    total_marks: float = Field(..., gt=0)
    passing_marks: Optional[float] = Field(None, ge=0)
    weightage: float = Field(default=1.0, ge=0, le=10)
    date: date
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    instructions: Optional[str] = None
    is_published: bool = False


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    total_marks: Optional[float] = Field(None, gt=0)
    passing_marks: Optional[float] = Field(None, ge=0)
    weightage: Optional[float] = Field(None, ge=0, le=10)
    date: Optional[date] = None
    due_date: Optional[date] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    instructions: Optional[str] = None
    is_published: Optional[bool] = None


class AssessmentResponse(AssessmentBase):
    id: int
    teacher_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Additional fields
    subject_name: Optional[str] = None
    teacher_name: Optional[str] = None
    total_submissions: Optional[int] = None
    graded_submissions: Optional[int] = None
    
    class Config:
        from_attributes = True


class GradeBase(BaseModel):
    student_id: int
    assessment_id: int
    marks_obtained: Optional[float] = Field(None, ge=0)
    is_absent: bool = False
    remarks: Optional[str] = None
    feedback: Optional[str] = None


class GradeCreate(GradeBase):
    subject_id: int


class GradeBulkCreate(BaseModel):
    """For grading multiple students for an assessment"""
    assessment_id: int
    subject_id: int
    grades: List[dict]  # [{student_id: int, marks_obtained: float, remarks: str}, ...]


class GradeUpdate(BaseModel):
    marks_obtained: Optional[float] = Field(None, ge=0)
    grade: Optional[GradeScale] = None
    is_absent: Optional[bool] = None
    remarks: Optional[str] = None
    feedback: Optional[str] = None


class GradeResponse(GradeBase):
    id: int
    subject_id: int
    teacher_id: int
    grade: Optional[GradeScale]
    percentage: Optional[float]
    submitted_on: Optional[datetime]
    graded_on: Optional[datetime]
    created_at: datetime
    
    # Additional fields
    student_name: Optional[str] = None
    assessment_title: Optional[str] = None
    subject_name: Optional[str] = None
    total_marks: Optional[float] = None
    
    class Config:
        from_attributes = True


class StudentGradesSummary(BaseModel):
    student_id: int
    student_name: str
    subject_id: int
    subject_name: str
    total_assessments: int
    completed_assessments: int
    total_marks: float
    marks_obtained: float
    percentage: float
    average_grade: Optional[str] = None
    
    class Config:
        from_attributes = True


class SubjectPerformanceResponse(BaseModel):
    subject_id: int
    subject_name: str
    total_students: int
    average_marks: float
    highest_marks: float
    lowest_marks: float
    passing_percentage: float
    
    class Config:
        from_attributes = True


class ReportCardBase(BaseModel):
    student_id: int
    class_id: int
    academic_year_id: int
    term: str
    conduct_grade: Optional[str] = None
    teacher_remarks: Optional[str] = None
    principal_remarks: Optional[str] = None


class ReportCardCreate(ReportCardBase):
    pass


class ReportCardResponse(ReportCardBase):
    id: int
    total_marks: Optional[float]
    marks_obtained: Optional[float]
    percentage: Optional[float]
    grade: Optional[str]
    rank: Optional[int]
    attendance_percentage: Optional[float]
    total_days: Optional[int]
    present_days: Optional[int]
    is_published: bool
    published_date: Optional[date]
    created_at: datetime
    
    class Config:
        from_attributes = True
