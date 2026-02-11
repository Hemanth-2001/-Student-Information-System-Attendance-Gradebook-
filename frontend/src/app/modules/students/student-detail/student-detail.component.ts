import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatChipsModule } from '@angular/material/chips';
import { Student } from '../../../models/student.model';
import { StudentService } from '../../../core/services/student.service';

@Component({
  selector: 'app-student-detail',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatTabsModule, MatChipsModule],
  template: `
    <div class="container" *ngIf="student">
      <h1>Student Details</h1>

      <mat-tab-group>
        <mat-tab label="Personal Information">
          <mat-card class="info-card">
            <div class="info-grid">
              <div class="info-item">
                <label>Admission Number</label>
                <p>{{ student.admission_number }}</p>
              </div>
              <div class="info-item">
                <label>Roll Number</label>
                <p>{{ student.roll_number || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Full Name</label>
                <p>{{ student.user?.first_name }} {{ student.user?.last_name }}</p>
              </div>
              <div class="info-item">
                <label>Email</label>
                <p>{{ student.user?.email }}</p>
              </div>
              <div class="info-item">
                <label>Date of Birth</label>
                <p>{{ student.date_of_birth | date }}</p>
              </div>
              <div class="info-item">
                <label>Gender</label>
                <p style="text-transform: capitalize;">{{ student.gender }}</p>
              </div>
              <div class="info-item">
                <label>Blood Group</label>
                <p>{{ student.blood_group || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Status</label>
                <mat-chip [color]="student.status === 'active' ? 'primary' : 'default'">
                  {{ student.status }}
                </mat-chip>
              </div>
            </div>
          </mat-card>
        </mat-tab>

        <mat-tab label="Contact Information">
          <mat-card class="info-card">
            <div class="info-grid">
              <div class="info-item">
                <label>Address Line 1</label>
                <p>{{ student.address_line1 || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Address Line 2</label>
                <p>{{ student.address_line2 || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>City</label>
                <p>{{ student.city || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>State</label>
                <p>{{ student.state || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Pincode</label>
                <p>{{ student.pincode || 'N/A' }}</p>
              </div>
              <div class="info-item">
                <label>Country</label>
                <p>{{ student.country }}</p>
              </div>
            </div>
          </mat-card>
        </mat-tab>

        <mat-tab label="Medical Information">
          <mat-card class="info-card">
            <div class="info-grid">
              <div class="info-item full-width">
                <label>Medical Conditions</label>
                <p>{{ student.medical_conditions || 'None' }}</p>
              </div>
              <div class="info-item full-width">
                <label>Allergies</label>
                <p>{{ student.allergies || 'None' }}</p>
              </div>
              <div class="info-item full-width">
                <label>Medications</label>
                <p>{{ student.medications || 'None' }}</p>
              </div>
            </div>
          </mat-card>
        </mat-tab>
      </mat-tab-group>
    </div>
  `,
  styles: [`
    .container {
      padding: 24px;
    }

    h1 {
      margin-bottom: 24px;
    }

    .info-card {
      margin: 16px;
      padding: 24px;
    }

    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 24px;
    }

    .info-item {
      display: flex;
      flex-direction: column;
    }

    .info-item.full-width {
      grid-column: 1 / -1;
    }

    .info-item label {
      font-weight: 500;
      color: #666;
      margin-bottom: 8px;
      font-size: 14px;
    }

    .info-item p {
      margin: 0;
      font-size: 16px;
      color: #333;
    }
  `]
})
export class StudentDetailComponent implements OnInit {
  student: Student | null = null;

  constructor(
    private route: ActivatedRoute,
    private studentService: StudentService
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.params['id'];
    this.loadStudent(id);
  }

  loadStudent(id: number) {
    this.studentService.getStudent(id).subscribe({
      next: (student) => {
        this.student = student;
      },
      error: (error) => {
        console.error('Error loading student:', error);
      }
    });
  }
}
