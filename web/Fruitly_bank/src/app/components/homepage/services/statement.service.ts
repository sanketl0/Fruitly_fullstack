import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/Envirnment/envirnment';

@Injectable({
  providedIn: 'root'
})
export class StatementService {

  envirnment =environment.apiUrl
  constructor(private http: HttpClient) {}


  // Get Account Statement List
  getAccountStatement(): Observable<any> {
    return this.http.get(`${this.envirnment}CIBPayment/AccountStatement/fetch-all-records/`);
  }

  // Get Credit Only Between Dates
  getCreditBetweenDates(fromDate: string, toDate: string): Observable<any> {
    // Construct the API endpoint with valid date parameters
    const apiUrl = `${this.envirnment}CIBPayment/AccountStatement/CreditOnly/BetweenDates/${fromDate}/${toDate}/`;
    console.log('Requesting data from:', apiUrl);  // For debugging
  
    return this.http.get(apiUrl);
  }

  // Get Split/Unsplit Remarks
  getSplitUnsplitRemarks(): Observable<any> {
    return this.http.get(`${this.envirnment}CIBPayment/AccountStatement/SplitUnsplitRemarks/`);
  }

  // Test Get Between Dates
  testGetBetweenDates(fromDate: string, toDate: string): Observable<any> {
    return this.http.get(
      `${this.envirnment}CIBPayment/AccountStatement/fetch-custom-records/${fromDate}/${toDate}/`
    );
  }

  gettodaysstament(fromDate: string, toDate: string): Observable<any>{
    return this.http.get(
      `${this.envirnment}CIBPayment/AccountStatement/fetch-todays-records/${fromDate}/${toDate}/`
    );
  }

  // Update Statement
  updateStatement(data: any): Observable<any> {
    return this.http.post(`${this.envirnment}CIBPayment/AccountStatement/UpdateStatement/`, data);
  }
  
}
