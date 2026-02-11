from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User, UserRole
from ..models.gradebook import Assessment, Grade, AssessmentType, GradeScale
from ..models.student import Student
from ..models.academic import Subject
from ..schemas.gradebook import (
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentResponse,
    GradeCreate,
    GradeBulkCreate,
    GradeUpdate,
    GradeResponse,
    StudentGradesSummary,
)

router = APIRouter(prefix="/gradebook", tags=["Gradebook"])


# ========== Assessment Endpoints ==========

@router.post("/assessments", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment_data: AssessmentCreate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new assessment (Test, Quiz, Assignment, etc.)"""
    # Get teacher ID
    teacher_id = None
    if current_user.role == UserRole.TEACHER:
        teacher_id = current_user.teacher_profile[0].id
    else:
        # For admin, we need to specify teacher_id in the request or default
        teacher_id = 1  # You might want to handle this differently
    
    new_assessment = Assessment(
        title=assessment_data.title,
        description=assessment_data.description,
        subject_id=assessment_data.subject_id,
        teacher_id=teacher_id,
        assessment_type=assessment_data.assessment_type,
        total_marks=assessment_data.total_marks,
        passing_marks=assessment_data.passing_marks,
        weightage=assessment_data.weightage,
        date=assessment_data.date,
        due_date=assessment_data.due_date,
        duration_minutes=assessment_data.duration_minutes,
        is_published=assessment_data.is_published,
        instructions=assessment_data.instructions,
    )
    
    db.add(new_assessment)
    await db.commit()
    await db.refresh(new_assessment)
    
    return new_assessment


@router.get("/assessments", response_model=List[AssessmentResponse])
async def list_assessments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    subject_id: Optional[int] = None,
    assessment_type: Optional[AssessmentType] = None,
    is_published: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all assessments with filters"""
    query = select(Assessment)
    
    if subject_id:
        query = query.where(Assessment.subject_id == subject_id)
    if assessment_type:
        query = query.where(Assessment.assessment_type == assessment_type)
    if is_published is not None:
        query = query.where(Assessment.is_published == is_published)
    
    # Teachers see only their assessments
    if current_user.role == UserRole.TEACHER:
        query = query.where(Assessment.teacher_id == current_user.teacher_profile[0].id)
    
    query = query.offset(skip).limit(limit).order_by(Assessment.date.desc())
    
    result = await db.execute(query)
    assessments = result.scalars().all()
    
    return assessments


@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assessment details by ID"""
    result = await db.execute(
        select(Assessment).where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    return assessment


@router.put("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def update_assessment(
    assessment_id: int,
    assessment_data: AssessmentUpdate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Update an assessment"""
    result = await db.execute(
        select(Assessment).where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Teachers can only update their own assessments
    if current_user.role == UserRole.TEACHER:
        if assessment.teacher_id != current_user.teacher_profile[0].id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this assessment"
            )
    
    update_data = assessment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assessment, field, value)
    
    await db.commit()
    await db.refresh(assessment)
    
    return assessment


@router.delete("/assessments/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assessment(
    assessment_id: int,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Delete an assessment"""
    result = await db.execute(
        select(Assessment).where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Teachers can only delete their own assessments
    if current_user.role == UserRole.TEACHER:
        if assessment.teacher_id != current_user.teacher_profile[0].id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this assessment"
            )
    
    await db.delete(assessment)
    await db.commit()
    
    return None


# ========== Grade Endpoints ==========

@router.post("/grades", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(
    grade_data: GradeCreate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Create a grade for a student"""
    # Get teacher ID
    teacher_id = None
    if current_user.role == UserRole.TEACHER:
        teacher_id = current_user.teacher_profile[0].id
    else:
        teacher_id = 1  # Handle differently for admin
    
    # Check if grade already exists
    result = await db.execute(
        select(Grade).where(
            and_(
                Grade.student_id == grade_data.student_id,
                Grade.assessment_id == grade_data.assessment_id
            )
        )
    )
    existing_grade = result.scalar_one_or_none()
    
    if existing_grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Grade already exists for this student and assessment"
        )
    
    # Get assessment to calculate percentage and grade
    assessment_result = await db.execute(
        select(Assessment).where(Assessment.id == grade_data.assessment_id)
    )
    assessment = assessment_result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Calculate percentage and letter grade
    percentage = None
    letter_grade = None
    if grade_data.marks_obtained is not None and not grade_data.is_absent:
        percentage = (grade_data.marks_obtained / assessment.total_marks) * 100
        letter_grade = calculate_letter_grade(percentage)
    
    new_grade = Grade(
        student_id=grade_data.student_id,
        assessment_id=grade_data.assessment_id,
        subject_id=grade_data.subject_id,
        teacher_id=teacher_id,
        marks_obtained=grade_data.marks_obtained,
        grade=letter_grade,
        percentage=percentage,
        is_absent=grade_data.is_absent,
        remarks=grade_data.remarks,
        feedback=grade_data.feedback,
        graded_on=datetime.now(),
    )
    
    db.add(new_grade)
    await db.commit()
    await db.refresh(new_grade)
    
    return new_grade


@router.post("/grades/bulk", status_code=status.HTTP_201_CREATED)
async def create_bulk_grades(
    grade_data: GradeBulkCreate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Create grades for multiple students at once"""
    teacher_id = None
    if current_user.role == UserRole.TEACHER:
        teacher_id = current_user.teacher_profile[0].id
    else:
        teacher_id = 1
    
    # Get assessment
    assessment_result = await db.execute(
        select(Assessment).where(Assessment.id == grade_data.assessment_id)
    )
    assessment = assessment_result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    created_count = 0
    
    for grade_record in grade_data.grades:
        # Check if grade already exists
        result = await db.execute(
            select(Grade).where(
                and_(
                    Grade.student_id == grade_record["student_id"],
                    Grade.assessment_id == grade_data.assessment_id
                )
            )
        )
        existing_grade = result.scalar_one_or_none()
        
        if not existing_grade:
            marks_obtained = grade_record.get("marks_obtained")
            is_absent = grade_record.get("is_absent", False)
            
            percentage = None
            letter_grade = None
            if marks_obtained is not None and not is_absent:
                percentage = (marks_obtained / assessment.total_marks) * 100
                letter_grade = calculate_letter_grade(percentage)
            
            new_grade = Grade(
                student_id=grade_record["student_id"],
                assessment_id=grade_data.assessment_id,
                subject_id=grade_data.subject_id,
                teacher_id=teacher_id,
                marks_obtained=marks_obtained,
                grade=letter_grade,
                percentage=percentage,
                is_absent=is_absent,
                remarks=grade_record.get("remarks"),
                graded_on=datetime.now(),
            )
            db.add(new_grade)
            created_count += 1
    
    await db.commit()
    
    return {"message": f"Grades created for {created_count} students"}


@router.get("/grades/student/{student_id}")
async def get_student_grades(
    student_id: int,
    subject_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all grades for a specific student"""
    # Check authorization
    if current_user.role == UserRole.STUDENT:
        if current_user.student_profile[0].id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this student's grades"
            )
    
    query = select(Grade).options(
        selectinload(Grade.assessment),
        selectinload(Grade.subject)
    ).where(Grade.student_id == student_id)
    
    if subject_id:
        query = query.where(Grade.subject_id == subject_id)
    
    query = query.order_by(Grade.graded_on.desc())
    
    result = await db.execute(query)
    grades = result.scalars().all()
    
    return grades


@router.get("/grades/assessment/{assessment_id}")
async def get_assessment_grades(
    assessment_id: int,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get all grades for a specific assessment"""
    query = select(Grade).options(
        selectinload(Grade.student).selectinload(Student.user)
    ).where(Grade.assessment_id == assessment_id)
    
    result = await db.execute(query)
    grades = result.scalars().all()
    
    return grades


@router.put("/grades/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade_data: GradeUpdate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Update a grade"""
    result = await db.execute(
        select(Grade).options(
            selectinload(Grade.assessment)
        ).where(Grade.id == grade_id)
    )
    grade = result.scalar_one_or_none()
    
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    
    # Teachers can only update their own grades
    if current_user.role == UserRole.TEACHER:
        if grade.teacher_id != current_user.teacher_profile[0].id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this grade"
            )
    
    update_data = grade_data.model_dump(exclude_unset=True)
    
    # Recalculate percentage and grade if marks changed
    if "marks_obtained" in update_data and update_data["marks_obtained"] is not None:
        percentage = (update_data["marks_obtained"] / grade.assessment.total_marks) * 100
        update_data["percentage"] = percentage
        update_data["grade"] = calculate_letter_grade(percentage)
    
    for field, value in update_data.items():
        setattr(grade, field, value)
    
    await db.commit()
    await db.refresh(grade)
    
    return grade


@router.delete("/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(
    grade_id: int,
    current_user: User = Depends(require_role("super_admin", "admin")),
    db: AsyncSession = Depends(get_db)
):
    """Delete a grade (Admin only)"""
    result = await db.execute(
        select(Grade).where(Grade.id == grade_id)
    )
    grade = result.scalar_one_or_none()
    
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )
    
    await db.delete(grade)
    await db.commit()
    
    return None


# ========== Helper Functions ==========

def calculate_letter_grade(percentage: float) -> GradeScale:
    """Calculate letter grade from percentage"""
    if percentage >= 90:
        return GradeScale.A_PLUS
    elif percentage >= 80:
        return GradeScale.A
    elif percentage >= 70:
        return GradeScale.B_PLUS
    elif percentage >= 60:
        return GradeScale.B
    elif percentage >= 50:
        return GradeScale.C_PLUS
    elif percentage >= 40:
        return GradeScale.C
    elif percentage >= 33:
        return GradeScale.D
    else:
        return GradeScale.F
