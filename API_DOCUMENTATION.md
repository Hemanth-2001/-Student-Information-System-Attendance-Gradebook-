# 📚 API Documentation

## Base URL

**Development:** `http://localhost:8000/api/v1`

**Production:** `https://api.schoolmanagement.com/api/v1`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_token_here>
```

### Get Token

**POST** `/auth/login`

```json
{
  "username": "admin",
  "password": "Admin@123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 👤 Authentication Endpoints

### Register User
**POST** `/auth/register`

```json
{
  "email": "student@school.com",
  "username": "student123",
  "password": "Student@123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890",
  "role": "student"
}
```

**Roles:** `super_admin`, `admin`, `teacher`, `student`, `parent`, `staff`

### Get Current User
**GET** `/auth/me`

Requires: Authentication

### Change Password
**POST** `/auth/change-password`

```json
{
  "old_password": "OldPass@123",
  "new_password": "NewPass@123"
}
```

---

## 🎓 Student Endpoints

### List Students
**GET** `/students?skip=0&limit=20&status=active&search=john`

**Query Parameters:**
- `skip` (int): Number of records to skip
- `limit` (int): Number of records to return
- `class_id` (int): Filter by class
- `section_id` (int): Filter by section
- `status` (string): active, inactive, graduated
- `search` (string): Search by name, email, admission number

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 5,
    "admission_number": "STU2024001",
    "roll_number": "10A-01",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@school.com",
    "class_name": "Class 10",
    "section_name": "A",
    "status": "active"
  }
]
```

### Get Student Details
**GET** `/students/{id}`

**Response:**
```json
{
  "id": 1,
  "user_id": 5,
  "admission_number": "STU2024001",
  "roll_number": "10A-01",
  "date_of_birth": "2010-05-15",
  "gender": "male",
  "blood_group": "A+",
  "nationality": "Indian",
  "address_line1": "123 Main Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "medical_conditions": "None",
  "allergies": "Peanuts",
  "class_id": 1,
  "section_id": 1,
  "admission_date": "2024-04-01",
  "status": "active"
}
```

### Create Student
**POST** `/students`

Requires: `super_admin` or `admin` role

```json
{
  "email": "new.student@school.com",
  "username": "newstudent",
  "password": "Student@123",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "9876543210",
  "admission_number": "STU2024002",
  "roll_number": "10B-15",
  "date_of_birth": "2010-08-20",
  "gender": "female",
  "blood_group": "O+",
  "nationality": "Indian",
  "address_line1": "456 Park Avenue",
  "city": "Delhi",
  "state": "Delhi",
  "pincode": "110001",
  "admission_date": "2024-04-01",
  "status": "active"
}
```

### Update Student
**PUT** `/students/{id}`

Requires: `super_admin` or `admin` role

```json
{
  "roll_number": "10B-16",
  "class_id": 2,
  "section_id": 3
}
```

### Delete Student
**DELETE** `/students/{id}`

Requires: `super_admin` or `admin` role

---

## 📅 Attendance Endpoints

### Mark Attendance (Single Student)
**POST** `/attendance`

```json
{
  "student_id": 1,
  "date": "2024-02-11",
  "status": "present",
  "remarks": "On time",
  "period_number": 1,
  "subject_id": 5,
  "check_in_time": "2024-02-11T09:00:00"
}
```

**Status Options:** `present`, `absent`, `late`, `half_day`, `sick_leave`, `excused`

### Mark Bulk Attendance
**POST** `/attendance/bulk`

```json
{
  "date": "2024-02-11",
  "period_number": 1,
  "subject_id": 5,
  "attendance_records": [
    { "student_id": 1, "status": "present" },
    { "student_id": 2, "status": "absent" },
    { "student_id": 3, "status": "late" }
  ]
}
```

### Get Attendance by Date
**GET** `/attendance/date/2024-02-11?class_id=1&section_id=2`

### Get Student Attendance
**GET** `/attendance/student/{student_id}?start_date=2024-02-01&end_date=2024-02-28`

### Get Attendance Statistics
**GET** `/attendance/stats/2024-02-11?class_id=1`

**Response:**
```json
{
  "total_students": 40,
  "present": 35,
  "absent": 3,
  "late": 2,
  "sick_leave": 0,
  "excused": 0,
  "half_day": 0,
  "attendance_percentage": 87.5
}
```

### Get Attendance Summary
**POST** `/attendance/summary`

```json
{
  "start_date": "2024-02-01",
  "end_date": "2024-02-28",
  "class_id": 1,
  "section_id": 2
}
```

**Response:**
```json
[
  {
    "student_id": 1,
    "student_name": "John Doe",
    "admission_number": "STU2024001",
    "total_days": 20,
    "present_days": 18,
    "absent_days": 1,
    "late_days": 1,
    "attendance_percentage": 90.0
  }
]
```

### Update Attendance
**PUT** `/attendance/{id}`

```json
{
  "status": "present",
  "remarks": "Late arrival, but present"
}
```

### Delete Attendance
**DELETE** `/attendance/{id}`

Requires: `super_admin` or `admin` role

---

## 📝 Gradebook Endpoints

### Create Assessment
**POST** `/gradebook/assessments`

```json
{
  "title": "Chapter 1 Quiz",
  "description": "Basic concepts quiz",
  "subject_id": 5,
  "assessment_type": "quiz",
  "total_marks": 50,
  "passing_marks": 20,
  "weightage": 1.0,
  "date": "2024-02-15",
  "due_date": "2024-02-15",
  "duration_minutes": 30,
  "is_published": true,
  "instructions": "Answer all questions"
}
```

**Assessment Types:** `assignment`, `quiz`, `test`, `mid_term`, `final_exam`, `project`, `practical`, `presentation`, `homework`

### List Assessments
**GET** `/gradebook/assessments?skip=0&limit=20&subject_id=5&assessment_type=quiz&is_published=true`

### Get Assessment Details
**GET** `/gradebook/assessments/{id}`

### Update Assessment
**PUT** `/gradebook/assessments/{id}`

### Delete Assessment
**DELETE** `/gradebook/assessments/{id}`

---

### Create Grade
**POST** `/gradebook/grades`

```json
{
  "student_id": 1,
  "assessment_id": 10,
  "subject_id": 5,
  "marks_obtained": 45,
  "is_absent": false,
  "remarks": "Good performance",
  "feedback": "Keep up the good work!"
}
```

**Automatic Calculations:**
- Percentage: Calculated from marks_obtained/total_marks
- Letter Grade: Assigned based on percentage (A+, A, B+, B, C+, C, D, F)

### Create Bulk Grades
**POST** `/gradebook/grades/bulk`

```json
{
  "assessment_id": 10,
  "subject_id": 5,
  "grades": [
    {
      "student_id": 1,
      "marks_obtained": 45,
      "remarks": "Excellent"
    },
    {
      "student_id": 2,
      "marks_obtained": 38,
      "remarks": "Good"
    },
    {
      "student_id": 3,
      "is_absent": true
    }
  ]
}
```

### Get Student Grades
**GET** `/gradebook/grades/student/{student_id}?subject_id=5`

### Get Assessment Grades
**GET** `/gradebook/grades/assessment/{assessment_id}`

**Response:**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "assessment_id": 10,
    "subject_id": 5,
    "teacher_id": 2,
    "marks_obtained": 45,
    "grade": "A",
    "percentage": 90.0,
    "is_absent": false,
    "remarks": "Excellent",
    "feedback": "Keep it up!",
    "graded_on": "2024-02-15T14:30:00",
    "student_name": "John Doe",
    "assessment_title": "Chapter 1 Quiz",
    "total_marks": 50
  }
]
```

### Update Grade
**PUT** `/gradebook/grades/{id}`

### Delete Grade
**DELETE** `/gradebook/grades/{id}`

---

## 🔐 Authorization Matrix

| Endpoint | super_admin | admin | teacher | student | parent |
|----------|-------------|-------|---------|---------|--------|
| Create Student | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Students | ✅ | ✅ | ✅ | Own Only | Children Only |
| Mark Attendance | ✅ | ✅ | ✅ | ❌ | ❌ |
| View Attendance | ✅ | ✅ | ✅ | Own Only | Children Only |
| Create Assessment | ✅ | ✅ | ✅ | ❌ | ❌ |
| Enter Grades | ✅ | ✅ | ✅ | ❌ | ❌ |
| View Grades | ✅ | ✅ | ✅ | Own Only | Children Only |

---

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (Delete success) |
| 400 | Bad Request (Validation error) |
| 401 | Unauthorized (No/Invalid token) |
| 403 | Forbidden (Insufficient permissions) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## 🔄 Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 📝 Notes

1. All dates should be in ISO format: `YYYY-MM-DD`
2. All timestamps should include timezone: `YYYY-MM-DDTHH:MM:SS`
3. All endpoints support pagination using `skip` and `limit` query parameters
4. Maximum page size is 100 records
5. Default page size is 20 records

---

## 🧪 Testing with Swagger

Interactive API documentation is available at:
- Development: http://localhost:8000/docs
- The Swagger UI allows you to test all endpoints directly

---

## 💡 Examples

### Complete Workflow: Student Registration to Grade Entry

1. **Register Student**
```bash
curl -X POST "http://localhost:8000/api/v1/students" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@school.com",
    "username": "student123",
    "password": "Student@123",
    "first_name": "John",
    "last_name": "Doe",
    "admission_number": "STU2024001",
    "date_of_birth": "2010-05-15",
    "gender": "male",
    "admission_date": "2024-04-01",
    "status": "active"
  }'
```

2. **Mark Attendance**
```bash
curl -X POST "http://localhost:8000/api/v1/attendance" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "date": "2024-02-11",
    "status": "present"
  }'
```

3. **Create Assessment**
```bash
curl -X POST "http://localhost:8000/api/v1/gradebook/assessments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Math Quiz 1",
    "subject_id": 1,
    "assessment_type": "quiz",
    "total_marks": 50,
    "date": "2024-02-15",
    "is_published": true
  }'
```

4. **Enter Grade**
```bash
curl -X POST "http://localhost:8000/api/v1/gradebook/grades" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "assessment_id": 1,
    "subject_id": 1,
    "marks_obtained": 45
  }'
```

---

For more details, visit the interactive documentation at `/docs`
