from . import URL
from Logger import logger
from ._base_class import APIBaseClass


class TransactionAPI(APIBaseClass):

    def __init__(self, data):
        super(TransactionAPI, self).__init__(data=data)
        self.url = URL.TransactionURL
        logger.debug(f"-------------Init TransactionAPI-------------: {self.url}")


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
