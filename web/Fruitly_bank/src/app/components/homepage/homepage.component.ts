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
  sortColumn: string = ''; // Track the currently sorted column
  sortDirection: 'asc' | 'desc' = 'asc'; // Track the sort direction
  totalDeposit: any;
  totalWithdrawal: any;
  loading: boolean = false;


  constructor(private api: HomeapiService,private router: Router,private stamentapi :StatementService,private authService: UserApiService) {}

  ngOnInit(): void {
    const userRole = this.getUserRole(); // Get user role
    this.getAccountStatement();
    this.getBalance(); 
    if (userRole !== 'user2') {
      
    }
  }
  
  getUserRole(): string {
    
    return localStorage.getItem('userRole') || ''; 
  }
  

  getBalance(): void {
    const userRole = this.authService.getUserRole();
    if (userRole === 'user2') {
      this.errorMessage = 'You do not have access to view the balance.';
      return;
    }
  
    this.loading = true; // Start loading
    this.errorMessage = ''; // Clear previous error messages
  
    this.api.fetchBalance().subscribe(
      (response) => {
        console.log('Balance data:', response);
        this.balanceData = response.body;
        this.loading = false; // Stop loading on success
      },
      (error) => {
        console.error('Error fetching balance:', error);
        this.loading = false; // Stop loading on error
  
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
  
  
  sortData(column: string) {
    if (this.sortColumn === column) {
      // Toggle sort direction if the same column is clicked again
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      // Sort by the new column in ascending order
      this.sortColumn = column;
      this.sortDirection = 'asc';
    }
  
    // Perform sorting based on the selected column
    if (column === 'srNo') {
      // Sorting for serial number is handled by column sorting
      this.customstatementData.sort((a, b) => {
        const indexA = this.customstatementData.indexOf(a);
        const indexB = this.customstatementData.indexOf(b);
        return this.sortDirection === 'asc' ? indexA - indexB : indexB - indexA;
      });
    } else if (column === 'Deposit (CR)' || column === 'Withdrawal (DR)') {
      // Sorting for Deposit and Withdrawal columns
      this.customstatementData.sort((a, b) => {
        const amountA = a.TYPE === (column === 'Deposit (CR)' ? 'CR' : 'DR') ? parseFloat(a.AMOUNT) : 0;
        const amountB = b.TYPE === (column === 'Deposit (CR)' ? 'CR' : 'DR') ? parseFloat(b.AMOUNT) : 0;
  
        if (amountA < amountB) {
          return this.sortDirection === 'asc' ? -1 : 1;
        }
        if (amountA > amountB) {
          return this.sortDirection === 'asc' ? 1 : -1;
        }
        return 0;
      });
    } else {
      // Sort by other columns (e.g., dateTime, TRANSACTIONID, REMARKS)
      this.customstatementData.sort((a, b) => {
        const valueA = a[column];
        const valueB = b[column];
  
        if (column === 'dateTime') {
          // For dateTime, convert to Date objects for proper comparison
          const dateA = new Date(a.TXNDATE);
          const dateB = new Date(b.TXNDATE);
  
          if (dateA < dateB) {
            return this.sortDirection === 'asc' ? -1 : 1;
          }
          if (dateA > dateB) {
            return this.sortDirection === 'asc' ? 1 : -1;
          }
          return 0;
        } else {
          // For other columns (e.g., TRANSACTIONID, REMARKS)
          if (valueA < valueB) {
            return this.sortDirection === 'asc' ? -1 : 1;
          }
          if (valueA > valueB) {
            return this.sortDirection === 'asc' ? 1 : -1;
          }
          return 0;
        }
      });
    }
  
    // After sorting, update the serial numbers
    this.updateSerialNumbers();
  }
  
  updateSerialNumbers() {
    this.customstatementData.forEach((item, index) => {
      item.srNo = this.sortDirection === 'asc' ? index + 1 : this.customstatementData.length - index;
    });
  }
  
  loadData() {
    // Sort data by dateTime in descending order (most recent first)
    this.customstatementData.sort((a, b) => {
      const dateA = new Date(a.TXNDATE);
      const dateB = new Date(b.TXNDATE);
      return dateB.getTime() - dateA.getTime(); // Descending order
    });
  
    // Initialize serial numbers when data is first loaded
    this.updateSerialNumbers();
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
    const userRole = this.authService.getUserRole();
    if (userRole === 'user2') {
      this.errorMessage = 'You do not have access to updates the statements.';
      return;
    }
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
    let toDate: Date = new Date(today); // Ensure toDate is set to today

    switch (range) {
      case 'past7Days':
        fromDate = new Date(today); // Clone today's date
        fromDate.setDate(today.getDate() - 6); // Go back 6 days (inclusive of today)
        break;
      case 'past5Days':
        fromDate = new Date(today); // Clone today's date
        fromDate.setDate(today.getDate() - 4); // Go back 4 days (inclusive of today)
        break;
      case 'last2Days':
        fromDate = new Date(today); // Clone today's date
        fromDate.setDate(today.getDate() - 1); // Go back 1 day (inclusive of today)
        break;
      case 'yesterday':
        fromDate = new Date(today); // Clone today's date
        fromDate.setDate(today.getDate() - 1); // Set to yesterday
        toDate = new Date(fromDate); // Yesterday as both from and to
        break;
      case 'today':
        // Directly call the bank API for today's data
        this.fetchTodayStatement();
        return;
      // case 'today':
      //   fromDate = new Date(today); // Set fromDate to today
      //   toDate = new Date(today);   // Set toDate to today
      //   break;
      default:
        this.errorMessage = 'Invalid date range selected.';
        return;
    }

    // Ensure fromDate is at 00:00:00 and toDate is at 23:59:59
    fromDate.setHours(0, 0, 0, 0);
    toDate.setHours(23, 59, 59, 999);

    // Format dates to YYYY-MM-DD (local time zone)
    const formattedFromDate = this.formatDateLocal(fromDate);
    const formattedToDate = this.formatDateLocal(toDate);

    console.log(`Fetching data from ${formattedFromDate} to ${formattedToDate}`);

    // Call method to fetch data
    this.getDatesBetween(formattedFromDate, formattedToDate);
  }


  fetchTodayStatement() {
    const today = new Date();
    const formattedToday = this.formatDateLocal(today);

    // Directly call the bank API for today's data
    this.stamentapi.gettodaysstament(formattedToday, formattedToday).subscribe(
        (response) => {
            if (response && response.data && response.data.length > 0) {
                let totalCR = 0;
                let totalDR = 0;

                this.customstatementData = response.data.map((item: any, index: number) => {
                    let amount = parseFloat(item.AMOUNT) || 0;
                    if (item.TYPE === "CR") {
                        totalCR += amount;
                    } else if (item.TYPE === "DR") {
                        totalDR += amount;
                    }

                    return {
                        ...item,
                        srNo: index + 1, // Assign Sr. No
                        dateOnly: item.TXNDATE ? item.TXNDATE.split('T')[0] : '',  // Extract date
                        timeOnly: item.TXNDATE ? this.formatTimeWithAMPM(item.TXNDATE) : '' // Extract time
                    };
                });

                // Store totals in variables to use in the table
                this.totalDeposit = Number(totalCR).toFixed(2);
                this.totalWithdrawal = Number(totalDR).toFixed(2);

                this.loadData();
            } else {
                this.errorMessage = 'No records found for today.';
                alert(this.errorMessage);
            }
        },
        (error) => {
            if (error.status === 403) {
                this.errorMessage = 'You do not have permission to perform this action.';
                alert(this.errorMessage);
            } else {
                this.errorMessage = 'Failed to fetch credit data.';
            }
            console.error(this.errorMessage, error);
        }
    );
 }

  formatDateLocal(date: Date): string {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
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
          let totalCR = 0;
          let totalDR = 0;
  
          this.customstatementData = response.data.map((item: any, index: number) => {
            let amount = parseFloat(item.AMOUNT) || 0;
            if (item.TYPE === "CR") {
              totalCR += amount;
            } else if (item.TYPE === "DR") {
              totalDR += amount;
            }
  
            return {
              ...item,
              srNo: index + 1, // Assign Sr. No
              dateOnly: item.TXNDATE ? item.TXNDATE.split('T')[0] : '',  // Extract date
              timeOnly: item.TXNDATE ? this.formatTimeWithAMPM(item.TXNDATE) : '' // Extract time
            };
          });
  
          // Store totals in variables to use in the table
          this.totalDeposit = Number(totalCR).toFixed(2);
          this.totalWithdrawal = Number(totalDR).toFixed(2);
  
          this.loadData();
        } else {
          this.errorMessage = 'No records found for the selected date range.';
          alert(this.errorMessage);
        }
      },
      (error) => {
        if (error.status === 403) {
          this.errorMessage = 'You do not have permission to perform this action.';
          alert(this.errorMessage);
        } else {
          this.errorMessage = 'Failed to fetch credit data.';
        }
        console.error(this.errorMessage, error);
      }
    );
  }

  
  
  
  
  formatTimeWithAMPM(dateString: string): string {
    const date = new Date(dateString);
    let hours: any = date.getHours();
    const minutes: any = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
  
    hours = hours % 12; // Convert to 12-hour format
    hours = hours ? hours : 12; // Handle 0 as 12
    const minutesFormatted = minutes < 10 ? '0' + minutes : minutes;
  
    return `${hours}:${minutesFormatted} ${ampm}`;
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
  
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
  
    // Prepare table data
    const tableData = this.customstatementData.map((item, index) => ({
      'Sr.no': index + 1,  
      'Date': item.dateOnly, 
      'Time': item.timeOnly,
      'TRANSACTION ID': item.TRANSACTIONID,
      'Remarks': item.REMARKS,
      'Deposit (CR)': item.TYPE === 'CR' ? item.AMOUNT : '', 
      'Withdrawal (DR)': item.TYPE === 'DR' ? item.AMOUNT : '' 
    }));
  
    // Add Total Row at the Top
    tableData.unshift({
      'Sr.no': 0,
      'Date': '',
      'Time': '',
      'TRANSACTION ID': '',
      'Remarks': '',
      'Deposit (CR)': this.totalDeposit,
      'Withdrawal (DR)': this.totalWithdrawal
    });
  
    const worksheet: XLSX.WorkSheet = XLSX.utils.json_to_sheet(tableData);
  
    // Apply styling for the header row
    const range = XLSX.utils.decode_range(worksheet['!ref']!);
    for (let C = range.s.c; C <= range.e.c; C++) {
      const headerCell = XLSX.utils.encode_cell({ r: 0, c: C });
      if (!worksheet[headerCell]) continue;
  
      worksheet[headerCell].s = {
        font: { bold: true, color: { rgb: "FFFFFF" } },  // White text
        fill: { fgColor: { rgb: "0000FF" } },  // Blue background
        alignment: { horizontal: "center" }
      };
    }
  
    worksheet['!cols'] = [
      { wch: 10 }, // Sr.no
      { wch: 15 }, // Date
      { wch: 10 }, // Time
      { wch: 25 }, // TRANSACTION ID
      { wch: 80 }, // Remarks
      { wch: 15 }, // Deposit (CR)
      { wch: 15 }  // Withdrawal (DR)
    ];
  
    const workbook: XLSX.WorkBook = { Sheets: { 'Statement': worksheet }, SheetNames: ['Statement'] };
    
    // Generate Excel file and trigger download
    const excelBuffer: any = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const data: Blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
    saveAs(data, `Transaction_Statement_${formattedDate}.xlsx`);
  }
  
  
  
  
  
  


}
