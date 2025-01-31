import datetime
import traceback

from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import BankAPI
from Logger import logger


class UATViewSet(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication]  # Token Authentication
    permission_classes = [IsAuthenticated]

    @action(detail=False, url_path='AccountStatementAPI')
    def call_account_statement_api(self, request):
        
        sample_data = {
            "AGGRID": "OTOE0480",
            # "AGGRNAME": "FRUITLY",
            "CORPID": "CIBNEXT",
            "USERID": "CIBTESTING6",
            "URN": "SR213835043",
            "ACCOUNTNO": "000405001257",
            "FROMDATE": "01-01-2016",
            "TODATE": "30-12-2016"
        }

        api = BankAPI.AccountStatementAPI(data=sample_data)
        response = api.call()
        if 200 <= response.status_code <= 299:
            decrypted_response = api.decrypt_response_data(method='Hybrid')
            return Response(decrypted_response)
        else:
            return Response(response.text, status=response.status_code)

    @action(detail=False, url_path='BalanceInquiryAPI')
    def call_balance_inquiry_api(self, request):
        # sample_data = {
        #     "AGGRID": "OTOE0480",
        #     "CORPID": "CIBNEXT",
        #     "USERID": "CIBTESTING6",
        #     "URN": "SR213835043",
        #     "ACCOUNTNO": "000405001257",
        # }

        sample_data = {
            "AGGRID": "OTOE0480",
            "CORPID": "582735465",
            "USERID": "NILESHSH",
            "URN": "SR213835043",
            "ACCOUNTNO": "346105001227",
        }

        try:
            api = BankAPI.BalanceInquiryAPI(data=sample_data)
            response = api.call()
            if 200 <= response.status_code <= 299:
                decrypted_response = api.decrypt_response_data(method='Basic')
                return Response(decrypted_response)
            else:
                logger.error(
                    f"Error response: {response.text} | status_code: {response.status_code}")
                return Response(response.text, status=response.status_code)

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(str(e), status=500)

    @action(detail=False, url_path='RegistrationStatusAPI')
    def call_registration_status_api(self, request):
        # sample_data = {
        #     "AGGRID": "OTOE0480",
        #     "AGGRNAME": "FRUITLY",
        #     "CORPID": "CIBNEXT",
        #     "USERID": "CIBTESTING6",
        #     "URN": "SR213835043"
        # }
        sample_data = {
            "AGGRID": "OTOE0480",
            "AGGRNAME": "FRUITLY",
            "CORPID": "582735465",
            "USERID": "NILESHSH",
            "URN": "SR213835043"
        }


        try:
            api = BankAPI.RegistrationStatusAPI(data=sample_data)
            response = api.call()
            if 200 <= response.status_code <= 299:
                decrypted_response = api.decrypt_response_data(method='Basic')
                return Response(decrypted_response)
            else:
                logger.error(
                    f"Error response: {response.text} | status_code: {response.status_code}")
                return Response(response.text, status=response.status_code)

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(str(e), status=500)

    @action(detail=False, url_path='TransactionAPI')
    def call_transaction_api(self, request):
        # sample_data = {
        #     "AGGRID": "OTOE0480",
        #     "AGGRNAME": "FRUITLY",
        #     "CORPID": "PRACHICIB1",
        #     "USERID": "USER3",
        #     "URN": "SR213835043",
        #     "UNIQUEID": "43566789699777",  # Some randome number
        #     "DEBITACC": "000451000301",
        #     "CREDITACC": "000405002777",
        #     "IFSC": "ICIC0000011",
        #     "AMOUNT": "4505.00",
        #     "CURRENCY": "INR",
        #     "TXNTYPE": "TPA",
        #     "PAYEENAME": "FruitlyTest",
        #     "WORKFLOW_REQD": "N"
        # }
        # sample_data = {               # For bank
        #     "AGGRID": "OTOE0480",
        #     "AGGRNAME": "FRUITLY",
        #     "CORPID": "582735465",
        #     "USERID": "NILESHSH",
        #     "URN": "SR213835043",
        #     "UNIQUEID": "4356678965235213",  # Some randome number
        #     "DEBITACC": "346105001227",
        #     "CREDITACC": "623801527379",
        #     "IFSC": "ICIC0000011",
        #     "AMOUNT": "1.00",
        #     "CURRENCY": "INR",
        #     "TXNTYPE": "TPA",
        #     "PAYEENAME": "Nilesh Shinolikar",
        #     "WORKFLOW_REQD": "Y"
        # }
        sample_data = {
            "AGGRID": "OTOE0480",
            "AGGRNAME": "FRUITLY",
            "CORPID": "CODERIZE15032016",
            "USERID": "NILESHS",
            "URN": "SR213835043",
            "UNIQUEID": "4356678965235213",  # Some randome number
            "DEBITACC": "187505000478",
            "CREDITACC": "623801527379",
            "IFSC": "ICIC0000011",
            "AMOUNT": "1.00",
            "CURRENCY": "INR",
            "TXNTYPE": "TPA",
            "PAYEENAME": "Nilesh Shinolikar",
            "WORKFLOW_REQD": "Y"
        }

        try:
            api = BankAPI.TransactionAPI(data=sample_data)
            response = api.call()
            if 200 <= response.status_code <= 299:
                decrypted_response = api.decrypt_response_data(method='Basic')
                return Response(decrypted_response)
            else:
                logger.error(
                    f"Error response: {response.text} | status_code: {response.status_code}")
                return Response(response.text, status=response.status_code)

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(str(e), status=500)

    @action(detail=False, url_path='TransactionInquiryAPI')
    def call_transaction_inquiry_api(self, request):
        from_transaction_api = {
    "CORP_ID": "582735465",
    "USER_ID": "NILESHSH",
    "AGGR_ID": "OTOE0480",
    "AGGR_NAME": "FRUITLY",
    "REQID": "738376855",
    "STATUS": "SUCCESS",
    "UNIQUEID": "4356678965235213",
    "URN": "SR213835043",
    "UTRNUMBER": "026475267581",
    "RESPONSE": "SUCCESS"
}
        # sample_data = {
        #     "AGGRID": "OTOE0480",
        #     "CORPID": "PRACHICIB1",
        #     "USERID": "USER3",
        #     "URN": "SR213835043",
        #     "UNIQUEID": "000451000301"
        # }
        sample_data = {
            "AGGRID": "OTOE0480",
            "CORPID": "582735465",
            "USERID": "NILESHSH",
            "URN": "SR213835043",
            "UNIQUEID": "4356678965235213"
        }


        try:
            api = BankAPI.TransactionInquiryAPI(data=sample_data)
            response = api.call()
            if 200 <= response.status_code <= 299:
                decrypted_response = api.decrypt_response_data(method='Basic')
                return Response(decrypted_response)
            else:
                logger.error(
                    f"Error response: {response.text} | status_code: {response.status_code}")
                return Response(response.text, status=response.status_code)

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(str(e), status=500)

    @action(detail=False, url_path='TestAll')
    def test_all_apis(self, request):
        funcs = [self.call_account_statement_api, self.call_balance_inquiry_api,
                 self.call_registration_status_api, self.call_transaction_api,
                 self.call_transaction_inquiry_api]

        for f in funcs:
            try:
                f(request._request)
            except Exception as e:
                pass

        return Response(f'TestComplete {datetime.datetime.now()}')
