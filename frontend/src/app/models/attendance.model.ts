export interface Attendance {
  id: number;
  student_id: number;
  date: string;
  status: AttendanceStatus;
  remarks?: string;
  period_number?: number;
  subject_id?: number;
  check_in_time?: string;
  check_out_time?: string;
  marked_by?: number;
  marked_at: string;
  student_name?: string;
}

export enum AttendanceStatus {
  PRESENT = 'present',
  ABSENT = 'absent',
  LATE = 'late',
  HALF_DAY = 'half_day',
  SICK_LEAVE = 'sick_leave',
  EXCUSED = 'excused'
}

export interface AttendanceCreate {
  student_id: number;
  date: string;
  status: AttendanceStatus;
  remarks?: string;
  period_number?: number;
  subject_id?: number;
  check_in_time?: string;
}

export interface AttendanceBulkCreate {
  date: string;
  period_number?: number;
  subject_id?: number;
  attendance_records: { student_id: number; status: string }[];
}

export interface AttendanceStats {
  total_students: number;
  present: number;
  absent: number;
  late: number;
  sick_leave: number;
  excused: number;
  half_day: number;
  attendance_percentage: number;
}

export interface StudentAttendanceSummary {
  student_id: number;
  student_name: string;
  admission_number: string;
  total_days: number;
  present_days: number;
  absent_days: number;
  late_days: number;
  attendance_percentage: number;
}
