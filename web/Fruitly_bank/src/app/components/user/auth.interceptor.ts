import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { UserApiService } from './user-api.service'; 
import { Router } from '@angular/router';
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private readonly TOKEN_KEY = 'authToken';

  constructor(private userApiService: UserApiService, private router: Router) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem(this.TOKEN_KEY);

    // Log the outgoing request
    console.log('Outgoing Request:', req);
    console.log('Outgoing token:', token);


    if (token) {
      const clonedRequest = req.clone({
        setHeaders: {
          Authorization: `Token ${token}`,
        },
      });

      return next.handle(clonedRequest).pipe(
        catchError((error) => this.handleError(error))
      );
    }

    return next.handle(req).pipe(
      catchError((error) => this.handleError(error))
    );
  }

  private handleError(error: any): Observable<never> {
    // if (error.status === 401) {
    //   // Handle token expiration or unauthorized request
    //   this.userApiService.logout();
    //   this.router.navigate(['/login']);
    // }
    console.error('Request Error:', error);
    // Return an observable with an error to propagate it
    return throwError(error);
  }
}