import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-student-form',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container">
      <h1>Add New Student</h1>
      <p>Student form component - To be implemented with full form fields</p>
    </div>
  `,
  styles: [`
    .container {
      padding: 24px;
    }
  `]
})
export class StudentFormComponent {}
