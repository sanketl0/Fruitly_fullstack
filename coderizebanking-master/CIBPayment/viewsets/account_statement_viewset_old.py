import datetime
import traceback
import pytz
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from datetime import datetime

from CIBPayment.models import AccountStatement, BankServerSync
from CIBPayment.serializers import AccountStatementSerializer, AccountStatementUpdateStatementSerializer

import BankAPI
from Logger import logger
from BankAPI.post_data_config import PostData
from accounts.permission import IsUser1OrUser2


class AccountStatementViewSet(viewsets.ViewSet):
    
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated,IsUser1OrUser2]
    
    @action(detail=False, url_path='fetch-all-records')
    def fetch_all_records(self, request):
        """
        Fetch all account statement records from the Bank API and store them in the database, avoiding duplicates.
        """
        tenant_name = request.tenant.name
        print(f"Tenant Name: {tenant_name}")

        # Prepare post data for the Bank API
        post_data = PostData(client_name=tenant_name)
        
        # Fetch records from the entire date range
        from_date = '01-01-2025'
        to_date = datetime.today().strftime('%d-%m-%Y')
        print("Today's date:", to_date)

        post_data = post_data.get_for_account_statement(from_date=from_date, to_date=to_date)

        try:
            print("___Post Data Sent to Bank API___:", post_data)
            # Call the Bank API
            api = BankAPI.AccountStatementAPI(data=post_data)
            response = api.call()
            print("_____API Response from Bank_____:", response.text)
            logger.debug(f"____All Statement Response____: {response.text}")

            if response.status_code == 200:
                # Decrypt the response data
                decrypted_response = api.decrypt_response_data(method='Hybrid')
                records = decrypted_response.get('Record', [])

                print("___Decrypted Records___:", records)

                if not records:
                    return Response({"message": "No new records found."})

                # Fetch existing TRANSACTIONIDs from DB to avoid duplicates
                existing_transaction_ids = set(AccountStatement.objects.values_list('TRANSACTIONID', flat=True))

                # Filter out records that already exist
                new_records = [
                    AccountStatement(
                        ACCOUNTNO=record.get('ACCOUNTNO', ''),
                        TXNDATE=datetime.strptime(record.get('TXNDATE'), '%d-%m-%Y %H:%M:%S'),
                        REMARKS=record.get('REMARKS', ''),
                        AMOUNT=float(record.get('AMOUNT').replace(',', '')),
                        BALANCE=float(record.get('BALANCE').replace(',', '')),
                        VALUEDATE=datetime.strptime(record.get('VALUEDATE'), '%d-%m-%Y').date(),
                        TYPE=record.get('TYPE', ''),
                        TRANSACTIONID=record.get('TRANSACTIONID', ''),
                        reconciliation_status='PENDING'
                    ) for record in records if record.get('TRANSACTIONID', '') not in existing_transaction_ids
                ]

                # Bulk insert only new records into the database
                if new_records:
                    AccountStatement.objects.bulk_create(new_records)
                    print(f"✅ Successfully stored {len(new_records)} new records in the database.")
                    return Response({"message": f"Fetched and stored {len(new_records)} new records."})
                else:
                    print("🔹 No new records to store.")
                    return Response({"message": "No new records found. All records already exist in the database."})

            else:
                print("❌ Failed to fetch data from Bank API")
                return Response({"error": "Failed to fetch data from Bank API"}, status=500)

        except Exception as e:
            print("🚨 Error:", str(e))
            return Response({"error": str(e)}, status=500)
   
 
   
   
    @action(detail=False, methods=['get'], url_path='fetch-custom-records/(?P<from_date>[^\.]+)/(?P<to_date>[^\.]+)')
    def fetch_custom_records(self, request, from_date, to_date):
        """
        Fetch custom account statement records. First search in the DB,
        if no records are found, then call the Bank API to fetch them.
        """
        # Ensure the dates are in the correct format (YYYY-MM-DD)
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            print(f"Received from_date: {from_date}, to_date: {to_date}")
        except ValueError:
            return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=400)

        # Search in the database first
        queryset = AccountStatement.objects.filter(VALUEDATE__range=[from_date, to_date])

        if queryset.exists():
            # If records are found in the database, serialize them
            serialized_data = AccountStatementSerializer(queryset, many=True).data
            return Response({"message": "Found records in the database.", "data": serialized_data})

        else:
            # If no records found in the database, fetch from the Bank API
            tenant_name = request.tenant.name
            print(f"Tenant Name: {tenant_name}")

            post_data = PostData(client_name=tenant_name)
            post_data = post_data.get_for_account_statement(from_date=from_date.strftime('%d-%m-%Y'),
                                                            to_date=to_date.strftime('%d-%m-%Y'))

            try:
                # Initialize the Bank API class and send the API request
                api = BankAPI.AccountStatementAPI(data=post_data)
                response = api.call()

                if response.status_code == 200:
                    # Decrypt the API response
                    decrypted_response = api.decrypt_response_data(method='Hybrid')
                    records = decrypted_response.get('Record', [])

                    if records:
                        # Fetch existing TRANSACTIONIDs from DB to avoid duplicates
                        existing_transaction_ids = set(AccountStatement.objects.values_list('TRANSACTIONID', flat=True))

                        # Filter out records that already exist
                        new_records = [
                            AccountStatement(
                                ACCOUNTNO=record.get('ACCOUNTNO', ''),
                                TXNDATE=datetime.strptime(record.get('TXNDATE'), '%d-%m-%Y %H:%M:%S'),
                                REMARKS=record.get('REMARKS', ''),
                                AMOUNT=float(record.get('AMOUNT', '0').replace(',', '')),
                                BALANCE=float(record.get('BALANCE', '0').replace(',', '')),
                                VALUEDATE=datetime.strptime(record.get('VALUEDATE'), '%d-%m-%Y').date(),
                                TYPE=record.get('TYPE', ''),
                                TRANSACTIONID=record.get('TRANSACTIONID', ''),
                                reconciliation_status='PENDING'
                            ) for record in records if record.get('TRANSACTIONID', '') not in existing_transaction_ids
                        ]


                        # Bulk insert only new records into the database
                        if new_records:
                            AccountStatement.objects.bulk_create(new_records)
                            print(f"✅ Successfully stored {len(new_records)} new records in the database.")

                            # Fetch newly stored records
                            queryset = AccountStatement.objects.filter(VALUEDATE__range=[from_date, to_date])
                            serialized_data = AccountStatementSerializer(queryset, many=True).data
                            return Response({"message": "Fetched from Bank API and stored in the database.", "data": serialized_data})
                        else:
                            return Response({"message": "No new records found. All records already exist in the database."})

                    else:
                        return Response({"message": "No records found from the Bank API."})

                else:
                    return Response({"error": "Failed to fetch data from Bank API"}, status=500)

            except Exception as e:
                return Response({"error": str(e)}, status=500)
    
    



    @action(detail=False, url_path=r'CreditOnly/BetweenDates/(?P<from_date>[^\.]+)/(?P<to_date>[^\.]+)')
    def get_credit_between_dates(self, request, from_date, to_date):
        """
        For Reconciliation
        Return only those transactions which have not been reconciled
        """
        queryset = AccountStatement.objects.filter(TYPE='CR',
                                                VALUEDATE__range=(from_date, to_date))
        return Response(AccountStatementSerializer(queryset, many=True).data)

    
    @action(detail=False, url_path='UpdateStatement')
    def update_table(self, request):
        """ To update new account statements into the database """
        logger.debug(f'-- API Call -- {request.path} | Headers: {request.headers} | Data: {request.data}')

        # If we pass TODATE, then it will take TODate otherwise it will take current date
        if request.GET.get('TODATE'):
            try:
                current_date = datetime.datetime.strptime(request.GET.get('TODATE'), "%Y-%m-%d").date()
            except Exception as e:
                return Response('Pass to date in YYYY-MM-DD format. {e}', status=400)
        else:
            # Get the current date
            current_date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date()

        if request.GET.get('FROMDATE'):
            try:
                last_date = datetime.datetime.strptime(request.GET.get('FROMDATE'), "%Y-%m-%d").date()
            except Exception as e:
                return Response('Pass from date in YYYY-MM-DD format. {e}', status=400)
        else:
            # Get the last date of account statement
            transaction_dates = AccountStatement.objects.values_list('TXNDATE', flat=True)
            if len(transaction_dates) == 0:
                last_date = current_date
            else:
                last_date = max(transaction_dates).date()

        # Here we are getting formatting the data to be send to Bank's APIs
        post_data = PostData(client_name=request.tenant.name)
        post_data = post_data.get_for_account_statement(from_date=str(last_date.strftime("%d-%m-%Y")),
                                                        to_date=str(current_date.strftime("%d-%m-%Y")))

        old_transaction_ids = AccountStatement.objects.values_list('TRANSACTIONID', flat=True)

        try:
            api = BankAPI.AccountStatementAPI(data=post_data)
            response = api.call()

            # Update last hit date
            server_sync_object, created = BankServerSync.objects.get_or_create(api='AccountStatementAPI')
            server_sync_object.number_of_hits += 1
            server_sync_object.save()

            # Check 1 if response code is not in 200
            if response.status_code >= 300:
                return Response(response.json(), status=response.status_code)

            decrypted_response = api.decrypt_response_data(method='Hybrid')

            # Check 2 if decrypted response return success
            if decrypted_response.get('RESPONSE') in ('FAILURE', 'Failure'):
                return Response(decrypted_response, status=400)

            # If all checks are complete, then process records

            # Update a success hit
            server_sync_object.last_successful_hit = timezone.now()
            server_sync_object.save()

            unique_records = []
            if isinstance(decrypted_response['Record'], list):
                for record in decrypted_response['Record']:
                    # Ignore records which are already there for last date
                    if record['TRANSACTIONID'] in old_transaction_ids:
                        continue

                    # Update account number in all fields
                    record['ACCOUNTNO'] = decrypted_response['ACCOUNTNO']
                    # Update user details
                    record['created_by'] = str(request.user)
                    # Remove commas from AMOUNT and BALANCE
                    record['AMOUNT'] = record['AMOUNT'].replace(",", "")
                    record['BALANCE'] = record['BALANCE'].replace(",", "")

                    unique_records.append(record)
            else:
                record = decrypted_response['Record']
                if record['TRANSACTIONID'] in old_transaction_ids:
                    pass
                else:
                    # Update account number in all fields
                    record['ACCOUNTNO'] = decrypted_response['ACCOUNTNO']
                    # Update user details
                    record['created_by'] = str(request.user)
                    # Remove commas from AMOUNT and BALANCE
                    record['AMOUNT'] = record['AMOUNT'].replace(",", "")
                    record['BALANCE'] = record['BALANCE'].replace(",", "")

                    unique_records.append(record)

            if len(unique_records) > 0:
                # Save the data to database
                serializer = AccountStatementUpdateStatementSerializer(data=unique_records, many=True)
                if serializer.is_valid():
                    serializer.save()

                    # Update a success hit
                    server_sync_object.last_successful_hit = timezone.now()
                    server_sync_object.save()

                    return Response({
                        "message": f"{len(unique_records)} New Records found and updated",
                        "last_successful_hit": str(timezone.localtime(server_sync_object.last_successful_hit)),
                        "data": serializer.data
                    })

                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response({
                    "message": "No new records found.",
                    "last_successful_hit": str(timezone.localtime(server_sync_object.last_successful_hit)),
                    "data": []
                })

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(str(e), status=500)



    @action(detail=False, url_path='SplitUnsplitRemarks')
    def split_unsplit_remarks(self, request):
            statement_rows = AccountStatement.objects.filter(remark_subtype__isnull=True)

            total_rows = len(statement_rows)
            for i, statement_row in enumerate(statement_rows):
                statement_row.split_remark()
                statement_row.save()

                print(f"[{i}/{total_rows}] - {i / total_rows * 100 :.2f}% - Done", end='\r')
            print("")

            return Response("Split Done")






















# /dummy
# @action(detail=False, url_path='TestGetBetweenDates')
# def test_get_between_dates(self, request):
#     logger.debug(f'-- API Call -- {request.path} | Headers: {request.headers} | Data: {request.data}')
    
#     # Extract 'from_date' and 'to_date' from query parameters
#     from_date = request.GET.get('from_date')
#     to_date = request.GET.get('to_date')
    
#     # Validate the presence of the dates
#     if not from_date or not to_date:
#         return Response(
#             {"error": "Both 'from_date' and 'to_date' query parameters are required."}, 
#             status=400
#         )
    
#     try:
#         # Validate and format the dates
#         from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").strftime("%d-%m-%Y")
#         to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").strftime("%d-%m-%Y")
#     except ValueError:
#         return Response(
#             {"error": "Dates must be in YYYY-MM-DD format."}, 
#             status=400
#         )
    
#     # Prepare post data
#     post_data = PostData(client_name=request.tenant.name)
#     api = BankAPI.AccountStatementAPI(
#         data=post_data.get_for_account_statement(from_date=from_date, to_date=to_date)
#     )
    
#     # Call the bank API and decrypt the response
#     response = api.call()
#     decrypted_response = api.decrypt_response_data(method='Hybrid')
    
#     return Response(decrypted_response)
