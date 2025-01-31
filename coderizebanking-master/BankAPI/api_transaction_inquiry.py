from . import URL
from Logger import logger
from ._base_class import APIBaseClass


class TransactionInquiryAPI(APIBaseClass):

    def __init__(self, data):
        super(TransactionInquiryAPI, self).__init__(data=data)
        self.url = URL.TransactionInquiryURL
        logger.debug(f"-------------Init TransactionInquiryAPI-------------: {self.url}")


if __name__ == '__main__':
    sample_data = {
        "AGGRID": "OTOE0480",
        "CORPID": "PRACHICIB1",
        "USERID": "USER3",
        "URN": "SR213835043",
        "UNIQUEID": "000451000301"
    }
