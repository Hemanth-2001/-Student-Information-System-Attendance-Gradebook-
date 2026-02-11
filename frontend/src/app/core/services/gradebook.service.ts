import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  Assessment,
  Grade,
  GradeCreate,
  StudentGradesSummary,
  AssessmentType
} from '../../models/gradebook.model';

@Injectable({
  providedIn: 'root'
})
export class GradebookService {
  private apiUrl = `${environment.apiUrl}/gradebook`;

  constructor(private http: HttpClient) {}

  // Assessment methods
  getAssessments(
    skip: number = 0,
    limit: number = 20,
    filters?: {
      subject_id?: number;
      assessment_type?: AssessmentType;
      is_published?: boolean;
    }
  ): Observable<Assessment[]> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    if (filters) {
      if (filters.subject_id) params = params.set('subject_id', filters.subject_id.toString());
      if (filters.assessment_type) params = params.set('assessment_type', filters.assessment_type);
      if (filters.is_published !== undefined) params = params.set('is_published', filters.is_published.toString());
    }

    return this.http.get<Assessment[]>(`${this.apiUrl}/assessments`, { params });
  }

  getAssessment(id: number): Observable<Assessment> {
    return this.http.get<Assessment>(`${this.apiUrl}/assessments/${id}`);
  }

  createAssessment(assessmentData: Partial<Assessment>): Observable<Assessment> {
    return this.http.post<Assessment>(`${this.apiUrl}/assessments`, assessmentData);
  }

  updateAssessment(id: number, assessmentData: Partial<Assessment>): Observable<Assessment> {
    return this.http.put<Assessment>(`${this.apiUrl}/assessments/${id}`, assessmentData);
  }

  deleteAssessment(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/assessments/${id}`);
  }

  // Grade methods
  createGrade(gradeData: GradeCreate): Observable<Grade> {
    return this.http.post<Grade>(`${this.apiUrl}/grades`, gradeData);
  }

  createBulkGrades(assessmentId: number, subjectId: number, grades: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/grades/bulk`, {
      assessment_id: assessmentId,
      subject_id: subjectId,
      grades: grades
    });
  }

  getStudentGrades(studentId: number, subjectId?: number): Observable<Grade[]> {
    let params = new HttpParams();
    if (subjectId) params = params.set('subject_id', subjectId.toString());

    return this.http.get<Grade[]>(`${this.apiUrl}/grades/student/${studentId}`, { params });
  }

  getAssessmentGrades(assessmentId: number): Observable<Grade[]> {
    return this.http.get<Grade[]>(`${this.apiUrl}/grades/assessment/${assessmentId}`);
  }

  updateGrade(id: number, gradeData: Partial<Grade>): Observable<Grade> {
    return this.http.put<Grade>(`${this.apiUrl}/grades/${id}`, gradeData);
  }

  deleteGrade(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/grades/${id}`);
  }
}
