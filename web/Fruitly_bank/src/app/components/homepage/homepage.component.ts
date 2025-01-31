import { Component, OnInit } from '@angular/core';
import { HomeapiService } from './services/homeapi.service';
import { Router } from '@angular/router';
import { StatementService } from './services/statement.service';
import { UserApiService } from '../user/user-api.service';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';


@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {

  balanceData: any;  
  errorMessage: string = '';  
  statementData: any[] = []; 
  fromDate: string = '';  
  toDate: string = '';    
  getfromDate: string = '';    
  gettoDate: string = '';    
  customstatementData: any[] = [];  



  constructor(private api: HomeapiService,private router: Router,private stamentapi :StatementService,private authService: UserApiService) {}

  ngOnInit(): void {
    this.getBalance(); 
    this.getAccountStatement() 
  }

  getBalance(): void {
    const userRole = this.authService.getUserRole();
    console.log(userRole)
  
    if (userRole !== 'user1') {
      this.errorMessage = 'You do not have access to view the balance.';
      return;
    }
  
    this.api.fetchBalance().subscribe(
      (response) => {
        console.log('Balance data:', response);
        this.balanceData = response.body;  
        this.errorMessage = ''; 
      },
      (error) => {
        console.error('Error fetching balance:', error);
        
        if (error?.error?.error?.errormessage) {
          this.errorMessage = `Success: ${error.error.error.success} <br>
                               Error Code: ${error.error.error.response} <br>
                               Error Message: ${error.error.error.errormessage}`;
        } else {
          this.errorMessage = 'Failed to fetch balance. Please try again later.';
        }
      }
    );
  }


  get dateAndTime() {
    if (this.balanceData && this.balanceData.DATE) {
      const dateTime = this.balanceData.DATE.split(' ');
      return {
        date: dateTime[0],  // Date part (YYYY-MM-DD)
        time: dateTime[1]   // Time part (HH:mm:ss)
      };
    }
    return { date: '', time: '' };
  }


  logout(): void {
    // Clear authentication token (log out the user)
    localStorage.removeItem('authToken');
    
    // Navigate to login page after logging out
    this.router.navigate(['/login']);
  }

  getAccountStatement(): void {
    this.stamentapi.getAccountStatement().subscribe({
      next: (data) => {
        this.statementData = data;  
      },
      error: (error) => {
        this.errorMessage = 'Error fetching account statement';  
        console.error('Error fetching account statement:', error);
      }
    });
  }



  getCreditData(fromDate: string, toDate: string) {
    // Check if the dates are empty or invalid
    if (!fromDate || !toDate) {
      this.errorMessage = 'Both From Date and To Date are required.';
      return;
    }
  
    // Proceed if the dates are valid
    const formattedFromDate = new Date(fromDate).toISOString().split('T')[0]; 
    const formattedToDate = new Date(toDate).toISOString().split('T')[0];
  
    this.stamentapi.getCreditBetweenDates(formattedFromDate, formattedToDate).subscribe(
      (data) => {
        this.statementData = data;
      },
      (error) => {
        this.errorMessage = 'Failed to fetch credit data';
        console.error(error);
      }
    );
  }
  



  getSplitUnsplitRemarks() {
    this.stamentapi.getSplitUnsplitRemarks().subscribe(
      (data) => {
        console.log('Split/Unsplit Remarks:', data);
      },
      (error) => {
        this.errorMessage = 'Failed to fetch remarks';
      }
    );
  }


  fetchStatement(range: string) {
    const today = new Date();
    let fromDate: Date;
    let toDate: Date;
  
    switch (range) {
      case 'past7Days':
        fromDate = new Date(today);
        fromDate.setDate(today.getDate() - 7);
        toDate = today;
        break;
      case 'past5Days':
        fromDate = new Date(today);
        fromDate.setDate(today.getDate() - 5);
        toDate = today;
        break;
      case 'last2Days':
        fromDate = new Date(today);
        fromDate.setDate(today.getDate() - 2);
        toDate = today;
        break;
      case 'yesterday':
        fromDate = new Date(today);
        fromDate.setDate(today.getDate() - 1);
        toDate = fromDate;
        break;
      case 'today':
        fromDate = today;
        toDate = today;
        break;
      default:
        this.errorMessage = 'Invalid date range selected.';
        return;
    }
  
    // Format dates to YYYY-MM-DD
    const formattedFromDate = fromDate.toISOString().split('T')[0];
    const formattedToDate = toDate.toISOString().split('T')[0];
  
    // Call the existing method to fetch data
    this.getDatesBetween(formattedFromDate, formattedToDate);
  }

  getDatesBetween(getfromDate: string, gettoDate: string) {
    if (!getfromDate || !gettoDate) {
      this.errorMessage = 'Both From Date and To Date are required.';
      console.log(this.errorMessage);
      return;
    }

    const formattedFromDate = new Date(getfromDate).toISOString().split('T')[0];
    const formattedToDate = new Date(gettoDate).toISOString().split('T')[0];
  
    this.stamentapi.testGetBetweenDates(formattedFromDate, formattedToDate).subscribe(
      (response) => {
        if (response && response.data && response.data.length > 0) {
          this.customstatementData = response.data;
        } else {
          this.errorMessage = 'No records found for the selected date range.';
        }
      },
      (error) => {
        this.errorMessage = 'Failed to fetch credit data';
        console.error(this.errorMessage, error);
      }
    );
    
  }
  
  

  updateStatement(data: any) {
    this.stamentapi.updateStatement(data).subscribe(
      (response) => {
        console.log('Statement Updated:', response);
      },
      (error) => {
        this.errorMessage = 'Failed to update statement';
      }
    );
  }


  exportToExcel(): void {
    if (!this.customstatementData || this.customstatementData.length === 0) {
      alert('No data available to download!');
      return;
    }
  
    // Generate today's date in YYYY-MM-DD format
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0]; // Extract YYYY-MM-DD
  
    // Convert the table data into JSON format
    const tableData = this.customstatementData.map(item => ({
      'TRANSACTION ID': item.TRANSACTIONID,
      'Amount': item.AMOUNT,
      'Type': item.TYPE,
      'Date': item.VALUEDATE,
      'Remarks': item.REMARKS
    }));
  
    // Create a worksheet
    const worksheet: XLSX.WorkSheet = XLSX.utils.json_to_sheet(tableData);
  
    // Set column widths
    worksheet['!cols'] = [
      { wch: 20 }, // TRANSACTION ID
      { wch: 15 }, // Amount
      { wch: 10 }, // Type
      { wch: 20 }, // Date
      { wch: 30 }  // Remarks
    ];
  
    const workbook: XLSX.WorkBook = { Sheets: { 'Statement': worksheet }, SheetNames: ['Statement'] };
    const excelBuffer: any = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const data: Blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(data, `Transaction_Statement_${formattedDate}.xlsx`);
  }
  
  
  


}
