import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatIconModule, MatButtonModule],
  template: `
    <div class="dashboard-container">
      <h1>Dashboard</h1>
      <p class="subtitle">Welcome to School Management System</p>

      <div class="cards-grid">
        <mat-card class="dashboard-card" (click)="navigate('/students')">
          <mat-card-header>
            <mat-icon class="card-icon students-icon">school</mat-icon>
            <mat-card-title>Students</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <h2 class="stat-number">1,234</h2>
            <p>Total Students</p>
          </mat-card-content>
        </mat-card>

        <mat-card class="dashboard-card" (click)="navigate('/attendance')">
          <mat-card-header>
            <mat-icon class="card-icon attendance-icon">event_available</mat-icon>
            <mat-card-title>Attendance</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <h2 class="stat-number">94.5%</h2>
            <p>Today's Attendance</p>
          </mat-card-content>
        </mat-card>

        <mat-card class="dashboard-card" (click)="navigate('/gradebook')">
          <mat-card-header>
            <mat-icon class="card-icon gradebook-icon">grade</mat-icon>
            <mat-card-title>Gradebook</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <h2 class="stat-number">156</h2>
            <p>Pending Assessments</p>
          </mat-card-content>
        </mat-card>

        <mat-card class="dashboard-card">
          <mat-card-header>
            <mat-icon class="card-icon teachers-icon">person</mat-icon>
            <mat-card-title>Teachers</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <h2 class="stat-number">85</h2>
            <p>Total Teachers</p>
          </mat-card-content>
        </mat-card>
      </div>

      <div class="recent-section">
        <mat-card>
          <mat-card-header>
            <mat-card-title>Quick Actions</mat-card-title>
          </mat-card-header>
          <mat-card-content>
            <div class="actions-grid">
              <button mat-raised-button color="primary" (click)="navigate('/students/new')">
                <mat-icon>add</mat-icon>
                Add Student
              </button>
              <button mat-raised-button color="primary" (click)="navigate('/attendance')">
                <mat-icon>check_circle</mat-icon>
                Mark Attendance
              </button>
              <button mat-raised-button color="primary" (click)="navigate('/gradebook')">
                <mat-icon>assignment</mat-icon>
                Create Assessment
              </button>
            </div>
          </mat-card-content>
        </mat-card>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 24px;
    }

    h1 {
      margin: 0 0 8px 0;
      font-size: 32px;
      color: #333;
    }

    .subtitle {
      margin: 0 0 32px 0;
      color: #666;
      font-size: 16px;
    }

    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 24px;
      margin-bottom: 32px;
    }

    .dashboard-card {
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .dashboard-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }

    .card-icon {
      font-size: 48px;
      width: 48px;
      height: 48px;
      margin-bottom: 8px;
    }

    .students-icon {
      color: #2196F3;
    }

    .attendance-icon {
      color: #4CAF50;
    }

    .gradebook-icon {
      color: #FF9800;
    }

    .teachers-icon {
      color: #9C27B0;
    }

    mat-card-header {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    mat-card-content {
      text-align: center;
    }

    .stat-number {
      font-size: 36px;
      font-weight: bold;
      margin: 16px 0 8px 0;
      color: #333;
    }

    .recent-section {
      margin-top: 32px;
    }

    .actions-grid {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }

    .actions-grid button {
      flex: 1;
      min-width: 200px;
    }

    .actions-grid button mat-icon {
      margin-right: 8px;
    }
  `]
})
export class DashboardComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit() {}

  navigate(path: string) {
    this.router.navigate([path]);
  }
}
