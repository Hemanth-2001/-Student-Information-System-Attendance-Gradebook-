import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Student, StudentListItem, StudentCreate } from '../../models/student.model';

@Injectable({
  providedIn: 'root'
})
export class StudentService {
  private apiUrl = `${environment.apiUrl}/students`;

  constructor(private http: HttpClient) {}

  getStudents(
    skip: number = 0,
    limit: number = 20,
    filters?: {
      class_id?: number;
      section_id?: number;
      status?: string;
      search?: string;
    }
  ): Observable<StudentListItem[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (filters) {
      if (filters.class_id) params = params.set('class_id', filters.class_id.toString());
      if (filters.section_id) params = params.set('section_id', filters.section_id.toString());
      if (filters.status) params = params.set('status', filters.status);
      if (filters.search) params = params.set('search', filters.search);
    }

    return this.http.get<StudentListItem[]>(this.apiUrl, { params });
  }

  getStudent(id: number): Observable<Student> {
    return this.http.get<Student>(`${this.apiUrl}/${id}`);
  }

  createStudent(studentData: StudentCreate): Observable<Student> {
    return this.http.post<Student>(this.apiUrl, studentData);
  }

  updateStudent(id: number, studentData: Partial<Student>): Observable<Student> {
    return this.http.put<Student>(`${this.apiUrl}/${id}`, studentData);
  }

  deleteStudent(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
