import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router); // Use the inject function to access services
  const isAuthenticated = !!localStorage.getItem('authToken'); // Check for authentication token

  if (!isAuthenticated) {
    // Redirect to login if not authenticated
    router.navigate(['/login']);
    return false;
  }
  return true;
};
