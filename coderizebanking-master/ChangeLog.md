## Server Version is 1.9.0

## ChangeLog:
### 1.9.1 (Future):
- 1.9.0.1 (07-09-2022):
  - Updated documentation

### 1.9.0 (17-08-2022):
- 1.8.0.1 (17-08-2022):
  - Fixed account statement update when only one record return

### 1.8.0 (17-08-2022):
- 1.7.0.2 (30-03-2022):
  - Added CodeRize Account Details
  - Tested Transaction in CodeRize account.

- 1.7.0.1 (15-03-2022):
  - Fixed Balance API

### 1.7.0 (11-03-2022):
- 1.6.0.2 (11-03-2022):
  - Changed account statement api to get data tenant wise
  - Deploying server to live 
  
- 1.6.0.1 (09-03-2022):
  - Project Cleanup
  - Tested for FruitBet
  - Moved API to BankAPI

### 1.6.0 (04-03-2022):
- 1.5.0.1 (04-03-2022):
  - Changed CIBPayment/AccountStatement/CreditOnly/BetweenDates/ API.
  - Removed Reconciled only check

### 1.5.0 (03-03-2022):
- 1.4.0.2 (03-03-2022):
  - Created CIBPayment/AccountStatement/CreditOnly/BetweenDates/ API
  - Fix private key hardcoded path
  - Return only those transactions which have not been reconciled

- 1.4.0.1 (02-03-2022):
  - Added vendor_location and customer_location

### 1.4.0 (03-02-2022):
- 1.3.0.1 (28-02-2022):
  - Changed some split logic in remark

### 1.3.0 (28-02-2022)
- 1.2.2.2 (28-02-2022):
  - Fixed issue when bank return data of previous weekend

- 1.2.2.1 (26-02-2022):
  - Added remark split logic
  - Added various fields to AccountStatement

### 1.2.2.0 (25-02-2022)
- 1.2.1.1 (25-02-2022):
  - Updated AccountStatementAPI to have records updated or not in response
  
### 1.2.1 (25-02-2022):
- 1.2.0.2 (25-02-2022):
  - Added BankServerSync model
  - Updated AccountStatementAPI and BalanceFetchAPI to update last hit time
  - Added BankServerSync APIs

- 1.2.0.1 (25-02-2022):
  - Added some logger fields in ECollection API
  - Update logger details to balance fetch API
  - Fixed date issue in Account statement update API

### 1.2.0 (25-02-2022):
- 1.1.12.1 (24-02-2022):
  - Added path for ICICIPublicKeyECollection
  - ECollection should be live now
  
### 1.1.12 (24-02-2022):
- 1.1.11.2 (24-02-2022):
  - Upgraded Account statement api
  - Added Balance API

- 1.1.11.1 (24-02-2022):
  - Added duplicate checker for account statement
  - Added auto before date and after date in account statement update api

### 1.1.11 (24-02-2022):
- 1.1.10.1 (24-02-2022):
  - Enabled CORS
  
### 1.1.10 (23-02-2022):
- 1.1.9.1 (23-02-2022):
  - Tested all CIB API, its live now

### 1.1.9 (22-02-2022):
- 1.1.8.2 (22-02-2022):
  - Changed TRANSACTIONID in Account statement to not be unique
- 1.1.8.1 (17-02-2022):
  - Updated API to save account statement to database

### 1.1.8 (17-02-2022)
- 1.0.7.2 (17-02-2022):
  - Going live
- 1.0.7.1 (16-02-2022):
  - Create seperate viewset for UAT
  - Installed swagger UI for API
  - Added a bit of documentation
  
### 1.0.7 (16-02-2022):
- 1.0.6.3 (16-02-2022):
  - split VirtualAccountNumber into customerid and custmer shortname
- 1.0.6.2 (16-02-2022):
  - Add field customer_id to transaction
  - Add field customer_shortname to transaction
  - Add field is_matched to transaction
  - Modified project to create different project files
  - Combined encryption decryption logic for both CIB and ECollection
- 1.0.6.1 (15-02-2022)
  - Minor Fixes and push
  - Added ObjectLog fields to ECollection

### 1.0.6 (14-02-2022):
- 1.0.5.2 (14-02-2022):
  - Added decryption logic for all APIs
  - Added logger for whole app
  - Added WSGI Logic
  - Updated django log_file_path
- 1.0.5.1 (11-02-2022):
  - Added Get account statement API
  - Added CIBPayment to installed apps and urls
  - Added Account Statement API
  - Added All five APIs
  - Created base class of API to confine all APIs

### 1.0.5 (10-02-2022):
  - Added Decryption logic for CIB Payments
  - Added API fro getting bank statement

### 1.0.4 (10-02-2022):
  - Fixed ECollection encryption
  - Added Changelog API

### 1.0.3 (09-02-2022):
- 1.0.3.1 (09-02-2022):
  - Removed slash from upi POST url
  - Added CIBPayment App
  - Created post request
  
### 1.0.2 (08-02-2022):
- 1.0.0.2 (08-02-2022):
  - Added Encrpytion and Decryption Logic in ECollection
  
### 1.0.1 (03-02-2022):
- 1.0.0.1 (03-02-2022):
  - Initial Project Setup
  - Created ECollection App
  - Created Transaction Model
  - Deploying first Beta version 
