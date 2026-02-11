import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { GradebookService } from '../../../core/services/gradebook.service';
import { Assessment, AssessmentType } from '../../../models/gradebook.model';

@Component({
  selector: 'app-gradebook-list',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule
  ],
  template: `
    <div class="container">
      <div class="header">
        <h1>Gradebook</h1>
        <button mat-raised-button color="primary">
          <mat-icon>add</mat-icon>
          Create Assessment
        </button>
      </div>

      <div class="filters">
        <mat-form-field appearance="outline">
          <mat-label>Assessment Type</mat-label>
          <mat-select [(ngModel)]="typeFilter" (ngModelChange)="loadAssessments()">
            <mat-option value="">All Types</mat-option>
            <mat-option value="assignment">Assignment</mat-option>
            <mat-option value="quiz">Quiz</mat-option>
            <mat-option value="test">Test</mat-option>
            <mat-option value="mid_term">Mid Term</mat-option>
            <mat-option value="final_exam">Final Exam</mat-option>
          </mat-select>
        </mat-form-field>
      </div>

      <div class="table-container">
        <table mat-table [dataSource]="assessments" class="gradebook-table">
          <ng-container matColumnDef="title">
            <th mat-header-cell *matHeaderCellDef>Title</th>
            <td mat-cell *matCellDef="let assessment">{{ assessment.title }}</td>
          </ng-container>

          <ng-container matColumnDef="type">
            <th mat-header-cell *matHeaderCellDef>Type</th>
            <td mat-cell *matCellDef="let assessment">
              <mat-chip>{{ formatType(assessment.assessment_type) }}</mat-chip>
            </td>
          </ng-container>

          <ng-container matColumnDef="totalMarks">
            <th mat-header-cell *matHeaderCellDef>Total Marks</th>
            <td mat-cell *matCellDef="let assessment">{{ assessment.total_marks }}</td>
          </ng-container>

          <ng-container matColumnDef="date">
            <th mat-header-cell *matHeaderCellDef>Date</th>
            <td mat-cell *matCellDef="let assessment">{{ assessment.date | date }}</td>
          </ng-container>

          <ng-container matColumnDef="status">
            <th mat-header-cell *matHeaderCellDef>Status</th>
            <td mat-cell *matCellDef="let assessment">
              <mat-chip [color]="assessment.is_published ? 'primary' : 'default'">
                {{ assessment.is_published ? 'Published' : 'Draft' }}
              </mat-chip>
            </td>
          </ng-container>

          <ng-container matColumnDef="actions">
            <th mat-header-cell *matHeaderCellDef>Actions</th>
            <td mat-cell *matCellDef="let assessment">
              <button mat-icon-button matTooltip="View Grades">
                <mat-icon>visibility</mat-icon>
              </button>
              <button mat-icon-button matTooltip="Grade Students">
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
      margin-bottom: 24px;
    }

    mat-form-field {
      max-width: 300px;
    }

    .table-container {
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow-x: auto;
    }

    .gradebook-table {
      width: 100%;
    }

    mat-chip {
      text-transform: capitalize;
    }
  `]
})
export class GradebookListComponent implements OnInit {
  assessments: Assessment[] = [];
  displayedColumns = ['title', 'type', 'totalMarks', 'date', 'status', 'actions'];
  typeFilter = '';

  constructor(
    private gradebookService: GradebookService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadAssessments();
  }

  loadAssessments() {
    this.gradebookService.getAssessments(0, 50, {
      assessment_type: (this.typeFilter as AssessmentType) || undefined
    }).subscribe({
      next: (assessments) => {
        this.assessments = assessments;
      },
      error: (error) => {
        console.error('Error loading assessments:', error);
      }
    });
  }

  formatType(type: string): string {
    return type.replace('_', ' ');
  }
}
