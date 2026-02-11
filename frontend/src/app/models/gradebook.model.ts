export interface Assessment {
  id: number;
  title: string;
  description?: string;
  subject_id: number;
  teacher_id: number;
  assessment_type: AssessmentType;
  total_marks: number;
  passing_marks?: number;
  weightage: number;
  date: string;
  due_date?: string;
  duration_minutes?: number;
  is_published: boolean;
  instructions?: string;
  created_at: string;
  updated_at?: string;
  subject_name?: string;
  teacher_name?: string;
  total_submissions?: number;
  graded_submissions?: number;
}

export enum AssessmentType {
  ASSIGNMENT = 'assignment',
  QUIZ = 'quiz',
  TEST = 'test',
  MID_TERM = 'mid_term',
  FINAL_EXAM = 'final_exam',
  PROJECT = 'project',
  PRACTICAL = 'practical',
  PRESENTATION = 'presentation',
  HOMEWORK = 'homework'
}

export interface Grade {
  id: number;
  student_id: number;
  assessment_id: number;
  subject_id: number;
  teacher_id: number;
  marks_obtained?: number;
  grade?: GradeScale;
  percentage?: number;
  is_absent: boolean;
  remarks?: string;
  feedback?: string;
  submitted_on?: string;
  graded_on?: string;
  created_at: string;
  student_name?: string;
  assessment_title?: string;
  subject_name?: string;
  total_marks?: number;
}

export enum GradeScale {
  A_PLUS = 'A+',
  A = 'A',
  B_PLUS = 'B+',
  B = 'B',
  C_PLUS = 'C+',
  C = 'C',
  D = 'D',
  F = 'F'
}

export interface GradeCreate {
  student_id: number;
  assessment_id: number;
  subject_id: number;
  marks_obtained?: number;
  is_absent: boolean;
  remarks?: string;
  feedback?: string;
}

export interface StudentGradesSummary {
  student_id: number;
  student_name: string;
  subject_id: number;
  subject_name: string;
  total_assessments: number;
  completed_assessments: number;
  total_marks: number;
  marks_obtained: number;
  percentage: number;
  average_grade?: string;
}
