import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { StudentService } from '../../../core/services/student.service';
import { StudentListItem } from '../../../models/student.model';

@Component({
  selector: 'app-student-list',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatChipsModule,
    FormsModule
  ],
  template: `
    <div class="container">
      <div class="header">
        <h1>Students</h1>
        <button mat-raised-button color="primary" (click)="navigateToAdd()">
          <mat-icon>add</mat-icon>
          Add Student
        </button>
      </div>

      <div class="filters">
        <mat-form-field appearance="outline">
          <mat-label>Search</mat-label>
          <input matInput [(ngModel)]="searchText" (ngModelChange)="loadStudents()" 
                 placeholder="Search by name, admission no., email">
          <mat-icon matPrefix>search</mat-icon>
        </mat-form-field>

        <mat-form-field appearance="outline">
          <mat-label>Status</mat-label>
          <mat-select [(ngModel)]="statusFilter" (ngModelChange)="loadStudents()">
            <mat-option value="">All</mat-option>
            <mat-option value="active">Active</mat-option>
            <mat-option value="inactive">Inactive</mat-option>
          </mat-select>
        </mat-form-field>
      </div>

      <div class="table-container">
        <table mat-table [dataSource]="students" class="student-table">
          <ng-container matColumnDef="admissionNumber">
            <th mat-header-cell *matHeaderCellDef>Admission No.</th>
            <td mat-cell *matCellDef="let student">{{ student.admission_number }}</td>
          </ng-container>

          <ng-container matColumnDef="name">
            <th mat-header-cell *matHeaderCellDef>Name</th>
            <td mat-cell *matCellDef="let student">
              {{ student.first_name }} {{ student.last_name }}
            </td>
          </ng-container>

          <ng-container matColumnDef="email">
            <th mat-header-cell *matHeaderCellDef>Email</th>
            <td mat-cell *matCellDef="let student">{{ student.email }}</td>
          </ng-container>

          <ng-container matColumnDef="class">
            <th mat-header-cell *matHeaderCellDef>Class</th>
            <td mat-cell *matCellDef="let student">
              {{ student.class_name || 'N/A' }} {{ student.section_name || '' }}
            </td>
          </ng-container>

          <ng-container matColumnDef="status">
            <th mat-header-cell *matHeaderCellDef>Status</th>
            <td mat-cell *matCellDef="let student">
              <mat-chip [color]="student.status === 'active' ? 'primary' : 'default'">
                {{ student.status }}
              </mat-chip>
            </td>
          </ng-container>

          <ng-container matColumnDef="actions">
            <th mat-header-cell *matHeaderCellDef>Actions</th>
            <td mat-cell *matCellDef="let student">
              <button mat-icon-button (click)="viewStudent(student.id)" matTooltip="View">
                <mat-icon>visibility</mat-icon>
              </button>
              <button mat-icon-button (click)="editStudent(student.id)" matTooltip="Edit">
                <mat-icon>edit</mat-icon>
              </button>
            </td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
        </table>
      </div>
    </div>
  `,
  styles: [`
    .container {
      padding: 24px;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }

    h1 {
      margin: 0;
      font-size: 28px;
    }

    .filters {
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
    }

    mat-form-field {
      flex: 1;
      max-width: 300px;
    }

    .table-container {
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow-x: auto;
    }

    .student-table {
      width: 100%;
    }

    mat-chip {
      text-transform: capitalize;
    }
  `]
})
export class StudentListComponent implements OnInit {
  students: StudentListItem[] = [];
  displayedColumns = ['admissionNumber', 'name', 'email', 'class', 'status', 'actions'];
  searchText = '';
  statusFilter = 'active';

  constructor(
    private studentService: StudentService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadStudents();
  }

  loadStudents() {
    this.studentService.getStudents(0, 50, {
      search: this.searchText || undefined,
      status: this.statusFilter || undefined
    }).subscribe({
      next: (students) => {
        this.students = students;
      },
      error: (error) => {
        console.error('Error loading students:', error);
      }
    });
  }

  navigateToAdd() {
    this.router.navigate(['/students/new']);
  }

  viewStudent(id: number) {
    this.router.navigate(['/students', id]);
  }

  editStudent(id: number) {
    this.router.navigate(['/students', id, 'edit']);
  }
}
