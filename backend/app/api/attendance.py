from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date, datetime

from ..core.database import get_db
from ..core.security import get_current_user, require_role
from ..models.user import User, UserRole
from ..models.attendance import Attendance, AttendanceStatus
from ..models.student import Student
from ..schemas.attendance import (
    AttendanceCreate,
    AttendanceBulkCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceStatsResponse,
    StudentAttendanceSummary,
    DateRangeAttendanceRequest,
)

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    attendance_data: AttendanceCreate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Mark attendance for a single student"""
    # Check if attendance already exists for this date
    result = await db.execute(
        select(Attendance).where(
            and_(
                Attendance.student_id == attendance_data.student_id,
                Attendance.date == attendance_data.date,
                Attendance.period_number == attendance_data.period_number
            )
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this date and period"
        )
    
    # Create attendance record
    new_attendance = Attendance(
        student_id=attendance_data.student_id,
        date=attendance_data.date,
        status=attendance_data.status,
        remarks=attendance_data.remarks,
        period_number=attendance_data.period_number,
        subject_id=attendance_data.subject_id,
        check_in_time=attendance_data.check_in_time or datetime.now(),
        marked_by=current_user.teacher_profile[0].id if current_user.role == UserRole.TEACHER else None,
    )
    
    db.add(new_attendance)
    await db.commit()
    await db.refresh(new_attendance)
    
    return new_attendance


@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def mark_bulk_attendance(
    attendance_data: AttendanceBulkCreate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Mark attendance for multiple students at once"""
    created_count = 0
    
    for record in attendance_data.attendance_records:
        # Check if already exists
        result = await db.execute(
            select(Attendance).where(
                and_(
                    Attendance.student_id == record["student_id"],
                    Attendance.date == attendance_data.date,
                    Attendance.period_number == attendance_data.period_number
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            new_attendance = Attendance(
                student_id=record["student_id"],
                date=attendance_data.date,
                status=AttendanceStatus(record["status"]),
                period_number=attendance_data.period_number,
                subject_id=attendance_data.subject_id,
                check_in_time=datetime.now(),
                marked_by=current_user.teacher_profile[0].id if current_user.role == UserRole.TEACHER else None,
            )
            db.add(new_attendance)
            created_count += 1
    
    await db.commit()
    
    return {"message": f"Attendance marked for {created_count} students"}


@router.get("/date/{attendance_date}")
async def get_attendance_by_date(
    attendance_date: date,
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance records for a specific date"""
    query = select(Attendance).options(
        selectinload(Attendance.student).selectinload(Student.user)
    ).where(Attendance.date == attendance_date)
    
    if class_id:
        query = query.join(Student).where(Student.class_id == class_id)
    if section_id:
        query = query.join(Student).where(Student.section_id == section_id)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    return records


@router.get("/student/{student_id}")
async def get_student_attendance(
    student_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance records for a specific student"""
    # Check authorization
    if current_user.role == UserRole.STUDENT and current_user.student_profile[0].id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this student's attendance"
        )
    
    query = select(Attendance).where(Attendance.student_id == student_id)
    
    if start_date:
        query = query.where(Attendance.date >= start_date)
    if end_date:
        query = query.where(Attendance.date <= end_date)
    
    query = query.order_by(Attendance.date.desc())
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    return records


@router.get("/stats/{attendance_date}", response_model=AttendanceStatsResponse)
async def get_attendance_stats(
    attendance_date: date,
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance statistics for a specific date"""
    query = select(Attendance).where(Attendance.date == attendance_date)
    
    if class_id:
        query = query.join(Student).where(Student.class_id == class_id)
    if section_id:
        query = query.join(Student).where(Student.section_id == section_id)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    total = len(records)
    present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
    absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
    late = sum(1 for r in records if r.status == AttendanceStatus.LATE)
    sick = sum(1 for r in records if r.status == AttendanceStatus.SICK_LEAVE)
    excused = sum(1 for r in records if r.status == AttendanceStatus.EXCUSED)
    half_day = sum(1 for r in records if r.status == AttendanceStatus.HALF_DAY)
    
    percentage = (present / total * 100) if total > 0 else 0
    
    return {
        "total_students": total,
        "present": present,
        "absent": absent,
        "late": late,
        "sick_leave": sick,
        "excused": excused,
        "half_day": half_day,
        "attendance_percentage": round(percentage, 2)
    }


@router.post("/summary")
async def get_attendance_summary(
    date_range: DateRangeAttendanceRequest,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance summary for students within a date range"""
    query = select(Student).options(selectinload(Student.user))
    
    if date_range.class_id:
        query = query.where(Student.class_id == date_range.class_id)
    if date_range.section_id:
        query = query.where(Student.section_id == date_range.section_id)
    
    result = await db.execute(query)
    students = result.scalars().all()
    
    summaries = []
    
    for student in students:
        attendance_query = select(Attendance).where(
            and_(
                Attendance.student_id == student.id,
                Attendance.date >= date_range.start_date,
                Attendance.date <= date_range.end_date
            )
        )
        
        att_result = await db.execute(attendance_query)
        records = att_result.scalars().all()
        
        total_days = len(records)
        present_days = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
        absent_days = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
        late_days = sum(1 for r in records if r.status == AttendanceStatus.LATE)
        
        percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        summaries.append({
            "student_id": student.id,
            "student_name": f"{student.user.first_name} {student.user.last_name}",
            "admission_number": student.admission_number,
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "late_days": late_days,
            "attendance_percentage": round(percentage, 2)
        })
    
    return summaries


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    current_user: User = Depends(require_role("super_admin", "admin", "teacher")),
    db: AsyncSession = Depends(get_db)
):
    """Update an attendance record"""
    result = await db.execute(
        select(Attendance).where(Attendance.id == attendance_id)
    )
    attendance = result.scalar_one_or_none()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    update_data = attendance_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attendance, field, value)
    
    await db.commit()
    await db.refresh(attendance)
    
    return attendance


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: int,
    current_user: User = Depends(require_role("super_admin", "admin")),
    db: AsyncSession = Depends(get_db)
):
    """Delete an attendance record (Admin only)"""
    result = await db.execute(
        select(Attendance).where(Attendance.id == attendance_id)
    )
    attendance = result.scalar_one_or_none()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    await db.delete(attendance)
    await db.commit()
    
    return None
