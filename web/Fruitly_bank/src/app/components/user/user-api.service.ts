import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, tap, throwError } from 'rxjs';
import { environment } from 'src/Envirnment/envirnment';

@Injectable({
  providedIn: 'root'
})
export class UserApiService {

  ennvirment =environment.apiUrl
  private TOKEN_KEY  = 'authToken';
  private readonly ROLE_KEY = 'userRole';


  constructor(private http: HttpClient) {}

  
  // Register user
  register(firstName: string, lastName: string, mobile_number: string, password: string, role: string): Observable<any> {
    const user = { first_name: firstName, last_name: lastName, mobile_number, password, role };
    return this.http.post(`${this.ennvirment}/accounts/register/`, user).pipe(
      catchError(error => {
        console.error('Registration error:', error);
        // Handle error appropriately (e.g., show a user-friendly message)
        return throwError(error);
      })
    );
  }
  

  login(mobile_number:string, password: string, role: string): Observable<any> {
    const loginData = { mobile_number, password, role };  // Include role in the login data
    return this.http.post(`${this.ennvirment}/accounts/login/`, loginData).pipe(
      tap((response: any) => {
        if (response && response.token) {
          this.saveToken(response.token);
          this.saverole(response.role);
        }
      }),
      catchError(error => {
        console.error('Login error:', error);
        // Handle login failure (e.g., invalid credentials)
        return throwError(error);
      })
    );
  }
  
  

  // // Send OTP (assuming this is for logging in)
  // sendOtp(email: string): Observable<any> {
  //   const otpData = { email };
  //   return this.http.post(`${this.ennvirment}/accounts/login/`, otpData);
  // }

  // // Verify OTP
  // verifyOtp(email: string, otp: string): Observable<any> {
  //   const otpData = { email, otp };
  //   return this.http.post(`${this.ennvirment}/accounts/validate-otp/`, otpData).pipe(
  //     tap((response: any) => {
  //       this.saveToken(response.token); // Save token after successful OTP validation
  //     })
  //   );
  // }

  // Store token in localStorage
  private saveToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY , token);
  }

  private saverole(role: string): void {
    localStorage.setItem(this.ROLE_KEY ,role);
  }


  getUserRole(): string {
    return localStorage.getItem(this.ROLE_KEY) || ''; // Get user role safely
  }
 
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  private getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY );
  }


  

  private removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    // this.router.navigate(['/login']);
  }
  
}
