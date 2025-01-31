from . import URL
from Logger import logger
from ._base_class import APIBaseClass
from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

class BalanceInquiryAPI(APIBaseClass):
    


    def __init__(self, data):
        # Pass the user_token to the parent class
        # self.user_token = user_token
        
        super(BalanceInquiryAPI, self).__init__(data=data)
        print("data to pass",self.data)
        self.url = URL.BalanceInquiryURL
        print("urlllllllllllll",self.url)
        logger.debug(f"-------------Init BalanceInquiryAPI-------------: {self.url}")


if __name__ == '__main__':
    sample_data = {
        "AGGRID": "OTOE0480",
        # "AGGRNAME": "FRUITLY",
        "CORPID": "CIBNEXT",
        "USERID": "CIBTESTING6",
        "URN": "SR213835043",
        "ACCOUNTNO": "000405001611",
        "FROMDATE": "01-01-2016",
        "TODATE": "30-12-2016"
    }
