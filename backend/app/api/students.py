from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional

from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User, UserRole
from ..models.student import Student
from ..models.academic import Class, Section
from ..schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentListResponse,
    StudentDetailResponse,
)

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    current_user: User = Depends(require_role("super_admin", "admin")),
    db: AsyncSession = Depends(get_db)
):
    """Create a new student (Admin only)"""
    # Check if admission number already exists
    result = await db.execute(
        select(Student).where(Student.admission_number == student_data.admission_number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admission number already exists"
        )
    
    # Check if email or username already exists
    result = await db.execute(
        select(User).where(
            (User.email == student_data.email) | (User.username == student_data.username)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already exists"
        )
    
    # Create user account
    from ..core.security import get_password_hash
    new_user = User(
        email=student_data.email,
        username=student_data.username,
        hashed_password=get_password_hash(student_data.password),
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        phone=student_data.phone,
        role=UserRole.STUDENT,
        is_active=True,
    )
    db.add(new_user)
    await db.flush()
    
    # Create student profile
    new_student = Student(
        user_id=new_user.id,
        admission_number=student_data.admission_number,
        roll_number=student_data.roll_number,
        date_of_birth=student_data.date_of_birth,
        gender=student_data.gender,
        blood_group=student_data.blood_group,
        nationality=student_data.nationality,
        religion=student_data.religion,
        category=student_data.category,
        address_line1=student_data.address_line1,
        address_line2=student_data.address_line2,
        city=student_data.city,
        state=student_data.state,
        pincode=student_data.pincode,
        country=student_data.country,
        medical_conditions=student_data.medical_conditions,
        allergies=student_data.allergies,
        medications=student_data.medications,
        emergency_contacts=student_data.emergency_contacts,
        class_id=student_data.class_id,
        section_id=student_data.section_id,
        admission_date=student_data.admission_date,
        previous_school=student_data.previous_school,
        status=student_data.status,
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    
    return new_student


@router.get("", response_model=List[StudentListResponse])
async def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    status: Optional[str] = "active",
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all students with filters"""
    query = select(Student).options(
        selectinload(Student.user),
        selectinload(Student.class_info),
        selectinload(Student.section)
    )
    
    # Apply filters
    if class_id:
        query = query.where(Student.class_id == class_id)
    if section_id:
        query = query.where(Student.section_id == section_id)
    if status:
        query = query.where(Student.status == status)
    if search:
        query = query.join(Student.user).where(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                Student.admission_number.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    students = result.scalars().all()
    
    # Format response
    response_list = []
    for student in students:
        response_list.append({
            "id": student.id,
            "user_id": student.user_id,
            "admission_number": student.admission_number,
            "roll_number": student.roll_number,
            "first_name": student.user.first_name,
            "last_name": student.user.last_name,
            "email": student.user.email,
            "class_name": student.class_info.name if student.class_info else None,
            "section_name": student.section.name if student.section else None,
            "status": student.status,
        })
    
    return response_list


@router.get("/{student_id}", response_model=StudentDetailResponse)
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get student details by ID"""
    result = await db.execute(
        select(Student)
        .options(selectinload(Student.user))
        .where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and current_user.id != student.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this student's information"
        )
    
    return student


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    current_user: User = Depends(require_role("super_admin", "admin")),
    db: AsyncSession = Depends(get_db)
):
    """Update student information (Admin only)"""
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Update fields
    update_data = student_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    await db.commit()
    await db.refresh(student)
    
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    current_user: User = Depends(require_role("super_admin", "admin")),
    db: AsyncSession = Depends(get_db)
):
    """Delete a student (Admin only)"""
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    await db.delete(student)
    await db.commit()
    
    return None
