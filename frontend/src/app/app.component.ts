import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { AuthService } from './core/services/auth.service';
import { User } from './models/user.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatSidenavModule,
    MatListModule
  ],
  template: `
    <div class="app-container" *ngIf="currentUser">
      <mat-sidenav-container class="sidenav-container">
        <mat-sidenav #sidenav mode="side" opened class="sidenav">
          <mat-nav-list>
            <a mat-list-item routerLink="/dashboard" routerLinkActive="active-link">
              <mat-icon>dashboard</mat-icon>
              <span>Dashboard</span>
            </a>
            <a mat-list-item routerLink="/students" routerLinkActive="active-link">
              <mat-icon>school</mat-icon>
              <span>Students</span>
            </a>
            <a mat-list-item routerLink="/attendance" routerLinkActive="active-link">
              <mat-icon>event_available</mat-icon>
              <span>Attendance</span>
            </a>
            <a mat-list-item routerLink="/gradebook" routerLinkActive="active-link">
              <mat-icon>grade</mat-icon>
              <span>Gradebook</span>
            </a>
          </mat-nav-list>
        </mat-sidenav>

        <mat-sidenav-content>
          <mat-toolbar color="primary">
            <button mat-icon-button (click)="sidenav.toggle()">
              <mat-icon>menu</mat-icon>
            </button>
            <span class="app-title">School Management System</span>
            <span class="spacer"></span>
            <button mat-button [matMenuTriggerFor]="userMenu">
              <mat-icon>account_circle</mat-icon>
              <span>{{ currentUser?.first_name }} {{ currentUser?.last_name }}</span>
            </button>
            <mat-menu #userMenu="matMenu">
              <button mat-menu-item routerLink="/profile">
                <mat-icon>person</mat-icon>
                <span>Profile</span>
              </button>
              <button mat-menu-item (click)="logout()">
                <mat-icon>exit_to_app</mat-icon>
                <span>Logout</span>
              </button>
            </mat-menu>
          </mat-toolbar>

          <div class="content-container">
            <router-outlet></router-outlet>
          </div>
        </mat-sidenav-content>
      </mat-sidenav-container>
    </div>

    <div *ngIf="!currentUser" class="login-container">
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    .app-container {
      height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .sidenav-container {
      flex: 1;
    }

    .sidenav {
      width: 250px;
      background-color: #f5f5f5;
    }

    .sidenav mat-nav-list a {
      display: flex;
      align-items: center;
      padding: 12px 16px;
    }

    .sidenav mat-icon {
      margin-right: 16px;
    }

    .active-link {
      background-color: #e3f2fd;
      color: #1976d2;
    }

    .spacer {
      flex: 1 1 auto;
    }

    .app-title {
      margin-left: 16px;
    }

    .content-container {
      padding: 24px;
      min-height: calc(100vh - 64px);
      background-color: #fafafa;
    }

    .login-container {
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
  `]
})
export class AppComponent implements OnInit {
  currentUser: User | null = null;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
