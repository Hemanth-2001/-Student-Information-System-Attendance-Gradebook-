import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { User, LoginRequest, AuthResponse } from '../../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    // Check if user is already logged in
    const token = this.getToken();
    if (token) {
      this.loadCurrentUser().subscribe();
    }
  }

  login(credentials: LoginRequest): Observable<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, formData).pipe(
      tap(response => {
        this.setToken(response.access_token);
        this.loadCurrentUser().subscribe();
      })
    );
  }

  register(userData: any): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/register`, userData);
  }

  logout(): void {
    this.removeToken();
    this.currentUserSubject.next(null);
  }

  loadCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/me`).pipe(
      tap(user => this.currentUserSubject.next(user))
    );
  }

  changePassword(oldPassword: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/change-password`, {
      old_password: oldPassword,
      new_password: newPassword
    });
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  setToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  removeToken(): void {
    localStorage.removeItem('access_token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }
}
