import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { FormsModule } from '@angular/forms';
import { AttendanceService } from '../../../core/services/attendance.service';
import { Attendance, AttendanceStats } from '../../../models/attendance.model';

@Component({
  selector: 'app-attendance-list',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    FormsModule
  ],
  template: `
    <div class="container">
      <h1>Attendance Management</h1>

      <div class="controls">
        <mat-form-field appearance="outline">
          <mat-label>Select Date</mat-label>
          <input matInput [matDatepicker]="picker" [(ngModel)]="selectedDate" 
                 (ngModelChange)="onDateChange()">
          <mat-datepicker-toggle matSuffix [for]="picker"></mat-datepicker-toggle>
          <mat-datepicker #picker></mat-datepicker>
        </mat-form-field>

        <button mat-raised-button color="primary" (click)="loadAttendance()">
          <mat-icon>refresh</mat-icon>
          Refresh
        </button>
      </div>

      <div class="stats-grid" *ngIf="stats">
        <mat-card class="stat-card present">
          <h3>{{ stats.present }}</h3>
          <p>Present</p>
        </mat-card>
        <mat-card class="stat-card absent">
          <h3>{{ stats.absent }}</h3>
          <p>Absent</p>
        </mat-card>
        <mat-card class="stat-card late">
          <h3>{{ stats.late }}</h3>
          <p>Late</p>
        </mat-card>
        <mat-card class="stat-card percentage">
          <h3>{{ stats.attendance_percentage }}%</h3>
          <p>Attendance Rate</p>
        </mat-card>
      </div>

      <div class="table-container">
        <table mat-table [dataSource]="attendanceRecords" class="attendance-table">
          <ng-container matColumnDef="studentName">
            <th mat-header-cell *matHeaderCellDef>Student Name</th>
            <td mat-cell *matCellDef="let record">{{ record.student_name }}</td>
          </ng-container>

          <ng-container matColumnDef="date">
            <th mat-header-cell *matHeaderCellDef>Date</th>
            <td mat-cell *matCellDef="let record">{{ record.date | date }}</td>
          </ng-container>

          <ng-container matColumnDef="status">
            <th mat-header-cell *matHeaderCellDef>Status</th>
            <td mat-cell *matCellDef="let record">
              <span [class]="'status-badge ' + record.status">
                {{ record.status }}
              </span>
            </td>
          </ng-container>

          <ng-container matColumnDef="checkIn">
            <th mat-header-cell *matHeaderCellDef>Check-In</th>
            <td mat-cell *matCellDef="let record">
              {{ record.check_in_time ? (record.check_in_time | date:'short') : 'N/A' }}
            </td>
          </ng-container>

          <ng-container matColumnDef="remarks">
            <th mat-header-cell *matHeaderCellDef>Remarks</th>
            <td mat-cell *matCellDef="let record">{{ record.remarks || '-' }}</td>
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

    h1 {
      margin-bottom: 24px;
    }

    .controls {
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
      align-items: center;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .stat-card {
      text-align: center;
      padding: 24px;
    }

    .stat-card h3 {
      font-size: 32px;
      margin: 0 0 8px 0;
    }

    .stat-card p {
      margin: 0;
      color: #666;
    }

    .stat-card.present {
      border-left: 4px solid #4CAF50;
    }

    .stat-card.absent {
      border-left: 4px solid #f44336;
    }

    .stat-card.late {
      border-left: 4px solid #FF9800;
    }

    .stat-card.percentage {
      border-left: 4px solid #2196F3;
    }

    .table-container {
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      overflow-x: auto;
    }

    .attendance-table {
      width: 100%;
    }

    .status-badge {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 500;
      text-transform: capitalize;
    }

    .status-badge.present {
      background-color: #E8F5E9;
      color: #2E7D32;
    }

    .status-badge.absent {
      background-color: #FFEBEE;
      color: #C62828;
    }

    .status-badge.late {
      background-color: #FFF3E0;
      color: #E65100;
    }
  `]
})
export class AttendanceListComponent implements OnInit {
  selectedDate = new Date();
  attendanceRecords: Attendance[] = [];
  stats: AttendanceStats | null = null;
  displayedColumns = ['studentName', 'date', 'status', 'checkIn', 'remarks'];

  constructor(private attendanceService: AttendanceService) {}

  ngOnInit() {
    this.loadAttendance();
  }

  onDateChange() {
    this.loadAttendance();
  }

  loadAttendance() {
    const dateStr = this.selectedDate.toISOString().split('T')[0];
    
    this.attendanceService.getAttendanceByDate(dateStr).subscribe({
      next: (records) => {
        this.attendanceRecords = records;
      },
      error: (error) => {
        console.error('Error loading attendance:', error);
      }
    });

    this.attendanceService.getAttendanceStats(dateStr).subscribe({
      next: (stats) => {
        this.stats = stats;
      },
      error: (error) => {
        console.error('Error loading stats:', error);
      }
    });
  }
}
