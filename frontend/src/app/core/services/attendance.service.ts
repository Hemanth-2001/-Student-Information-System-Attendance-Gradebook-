import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  Attendance,
  AttendanceCreate,
  AttendanceBulkCreate,
  AttendanceStats,
  StudentAttendanceSummary
} from '../../models/attendance.model';

@Injectable({
  providedIn: 'root'
})
export class AttendanceService {
  private apiUrl = `${environment.apiUrl}/attendance`;

  constructor(private http: HttpClient) {}

  markAttendance(attendanceData: AttendanceCreate): Observable<Attendance> {
    return this.http.post<Attendance>(this.apiUrl, attendanceData);
  }

  markBulkAttendance(attendanceData: AttendanceBulkCreate): Observable<any> {
    return this.http.post(`${this.apiUrl}/bulk`, attendanceData);
  }

  getAttendanceByDate(
    date: string,
    classId?: number,
    sectionId?: number
  ): Observable<Attendance[]> {
    let params = new HttpParams();
    if (classId) params = params.set('class_id', classId.toString());
    if (sectionId) params = params.set('section_id', sectionId.toString());

    return this.http.get<Attendance[]>(`${this.apiUrl}/date/${date}`, { params });
  }

  getStudentAttendance(
    studentId: number,
    startDate?: string,
    endDate?: string
  ): Observable<Attendance[]> {
    let params = new HttpParams();
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);

    return this.http.get<Attendance[]>(`${this.apiUrl}/student/${studentId}`, { params });
  }

  getAttendanceStats(
    date: string,
    classId?: number,
    sectionId?: number
  ): Observable<AttendanceStats> {
    let params = new HttpParams();
    if (classId) params = params.set('class_id', classId.toString());
    if (sectionId) params = params.set('section_id', sectionId.toString());

    return this.http.get<AttendanceStats>(`${this.apiUrl}/stats/${date}`, { params });
  }

  getAttendanceSummary(
    startDate: string,
    endDate: string,
    classId?: number,
    sectionId?: number
  ): Observable<StudentAttendanceSummary[]> {
    return this.http.post<StudentAttendanceSummary[]>(`${this.apiUrl}/summary`, {
      start_date: startDate,
      end_date: endDate,
      class_id: classId,
      section_id: sectionId
    });
  }

  updateAttendance(id: number, attendanceData: Partial<Attendance>): Observable<Attendance> {
    return this.http.put<Attendance>(`${this.apiUrl}/${id}`, attendanceData);
  }

  deleteAttendance(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
