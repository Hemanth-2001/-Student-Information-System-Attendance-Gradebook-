import { Routes } from '@angular/router';
import { authGuard, roleGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./modules/auth/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./modules/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: 'students',
    loadComponent: () => import('./modules/students/student-list/student-list.component').then(m => m.StudentListComponent),
    canActivate: [authGuard]
  },
  {
    path: 'students/:id',
    loadComponent: () => import('./modules/students/student-detail/student-detail.component').then(m => m.StudentDetailComponent),
    canActivate: [authGuard]
  },
  {
    path: 'students/new',
    loadComponent: () => import('./modules/students/student-form/student-form.component').then(m => m.StudentFormComponent),
    canActivate: [authGuard, roleGuard],
    data: { roles: ['super_admin', 'admin'] }
  },
  {
    path: 'attendance',
    loadComponent: () => import('./modules/attendance/attendance-list/attendance-list.component').then(m => m.AttendanceListComponent),
    canActivate: [authGuard]
  },
  {
    path: 'gradebook',
    loadComponent: () => import('./modules/gradebook/gradebook-list/gradebook-list.component').then(m => m.GradebookListComponent),
    canActivate: [authGuard]
  },
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
