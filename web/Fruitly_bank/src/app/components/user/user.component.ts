import { Component } from '@angular/core';
import { UserApiService } from './user-api.service';
import { environment } from 'src/Envirnment/envirnment';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent {

  firstName: string = '';
  lastName: string = '';
  mobile_number:any;
  password: string = '';
  role: string = 'user2';  // Default role
  otp: string = '';
  isOtpSent: boolean = false;
  isOtpVerified: boolean = false;
  isLoginEnabled: boolean = false;  
  errorMessage: string = '';
  successMessage: string = '';
  roles: string[] = ['user1', 'user2', 'admin']; 
  roleSelected: boolean = false;  
  selectedRole: string = '';  
  isFirstTimeUser: boolean = false;

  constructor(private authService: UserApiService,private http: HttpClient,private router: Router) {
    this.isFirstTimeUser = !localStorage.getItem('authToken');
    const storedRole = localStorage.getItem('userRole');
    if (storedRole) {
      this.selectedRole = storedRole;
      this.roleSelected = true;  // Skip role selection
    }

    // Redirect to last visited page if logged in
  const lastPage = localStorage.getItem('lastVisitedPage');
  if (this.authService.isLoggedIn() && lastPage) {
    this.router.navigateByUrl(lastPage);
  }
  }

  selectRole(role: string): void {
    this.selectedRole = role;
    this.roleSelected = true;
    localStorage.setItem('userRole', role); // Save role to localStorage

  }

  

  // register(): void {
  //   this.authService
  //     .register(this.firstName, this.lastName, this.mobile_number, this.password, this.selectedRole)
  //     .subscribe(
  //       (response) => {
  
  //         if (this.selectedRole === 'user1' || this.selectedRole === 'user2') {
  //           localStorage.setItem('userRole', this.selectedRole);
  //           alert('User registered successfully, pending admin approval');
  //         } else {
  //           alert('Admin registered successfully with full access');
  //         }
  //       },
  //       (error) => {
  //         console.error('Error during registration:', error);
  //         alert('Registration failed');
  //       }
  //     );
  // }
  
  register(): void {
    this.authService
      .register(this.firstName, this.lastName, this.mobile_number, this.password, this.selectedRole)
      .subscribe(
        (response) => {
          localStorage.setItem('userRole', this.selectedRole);  // Store role in localStorage
          alert('User registered successfully, pending admin approval');
        },
        (error) => {
          console.error('Error during registration:', error);
          alert('Registration failed');
        }
      );
  }

  login() {
    this.authService.login(this.mobile_number, this.password, this.selectedRole).subscribe(
      (response: any) => {  
        if (response && response.token) {
          localStorage.setItem('authToken', response.token);
          localStorage.setItem('userRole', this.selectedRole);  // Save role on login
          this.router.navigate(['/home']);
        } else {
          alert('Failed to login. Please try again.');
        }
      },
      (error) => {
        console.error('Login error: ', error);
        let errorMessage = 'An unexpected error occurred. Please try again later.';
  
        if (error.status === 400) {
          // Distinguish between different 400 errors
          if (error.error && error.error.error === 'Invalid email or password') {
            errorMessage = 'Invalid email or password. Please check your credentials and try again.';
          } else {
            errorMessage = 'Email, password, and role are required.';
          }
        } 
        else if (error.status === 403) {
          if (error.error.error === 'Your account is pending approval by the admin') {
            errorMessage = 'Your account is pending admin approval. Please wait for approval before logging in.';
          } 
          else if (error.error.error === 'Your account is inactive') {
            errorMessage = 'Your account is inactive. Please contact support.';
          }
        }
  
        alert(errorMessage);
      }
    );
  }
  
  
  
  

  goBack(): void {
    this.roleSelected = false;  // Reset the role selection step
    localStorage.removeItem('userRole'); // Remove role from localStorage if going back
    this.firstName = '';
    this.lastName = '';
    this.mobile_number = '';
    this.password = '';
    this.otp = '';
    this.isOtpSent = false;
    this.isOtpVerified = false;
  }
 
  

}
