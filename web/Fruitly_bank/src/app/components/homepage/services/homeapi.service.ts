import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, Observable, tap, throwError } from 'rxjs';
import { environment } from 'src/Envirnment/envirnment';

@Injectable({
  providedIn: 'root'
})
export class HomeapiService {

  envirnment =environment.apiUrl
  baseurl =environment.apiUrl
  constructor(private http: HttpClient) {}

  fetchBalance(): Observable<any> {
  console.log('Preparing request with token');

  // Assuming you have a method to get the token (e.g., from localStorage or an auth service)
  const token = 'YOUR_TOKEN_HERE'; // Replace with actual token or fetch from a service

  // Set the headers including the token
  const headers = new HttpHeaders({
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  });

  return this.http.get(`${environment.apiUrl}CIBPayment/Balance/Fetch/`, {
    headers: headers, // Pass headers in the request
    observe: 'response'
  }).pipe(
    tap(response => {
      console.log('API Response:', response); 
    }),
    catchError(error => {
      console.error('API Error:', error); 
      return throwError(error);
    })
  );
}

  // updateTransactionType(transactionId: string, transactionType: string): Observable<any> {
  //   return this.http.patch(`${this.baseurl}CIBPayment/AccountStatement/update-transaction-type/${transactionId}/`, {
  //     transaction_type: transactionType
  //   });
  // }

  updateTransactionType(transactionId: string, transactionType: string): Observable<any> {
    return this.http.patch(`${this.baseurl}CIBPayment/AccountStatement/${transactionId}/update-transaction-type/`, {
      transaction_type: transactionType
    });
  }




}
