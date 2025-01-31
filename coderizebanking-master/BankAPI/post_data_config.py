"""
Author: Nitish Patel
Date: 2022-05-01
"""

class PostData:
    """
    This class is used to contain and format data to sent to Bank's API.
    As if more than or less than required data in sent to the server, it will throw error
    """

    # def __init__(self, client_name):

    #     common_data = {"AGGRID": "OTOE0480",
    #                    #    "CORPID": "582735465",
    #                    #    "USERID": "NILESHSH",
    #                    "URN": "SR213835043",
    #                    #    "ACCOUNTNO": "346105001227"
    #                    }

    #     # Tenant name should be same as client name
    #     if client_name == 'Fruitly':
    #         variable_data = {"CORPID": "582735465",
    #                          "USERID": "NILESHSH",
    #                          "ACCOUNTNO": "346105001227"}
            
    #     elif client_name == 'Fruitbet':
    #         variable_data = {"CORPID": "582745673",
    #                          "USERID": "NILESHSH",
    #                          "ACCOUNTNO": "346105001228"}
            
    #     elif client_name == 'CodeRize':
    #         variable_data = {"CORPID": "CODERIZE15032016",
    #                          "USERID": "NILESHS",
    #                          "ACCOUNTNO": "187505000478"}
        
    #     elif client_name == 'Public Tenant':  
    #         variable_data = {"CORPID": "582735465",
    #                          "USERID": "NILESHSH",
    #                          "ACCOUNTNO": "346105001227"}
        
    #     else:
    #         raise Exception(f"client_name not found: {client_name}")

    #     # Combining variable data with common data
    #     common_data.update(variable_data)
    #     self.data = common_data
    
    
    def __init__(self, client_name):
        # Normalize client_name to remove extra spaces or special characters
        client_name = client_name.strip().replace('\xa0', ' ')  # \xa0 is a no-break space

        common_data = {"AGGRID": "OTOE0480", "URN": "SR213835043"}

        tenant_map = {
            'Fruitly': {"CORPID": "582735465", "USERID": "NILESHSH", "ACCOUNTNO": "346105001227"},
            'Fruitbet': {"CORPID": "582745673", "USERID": "NILESHSH", "ACCOUNTNO": "346105001228"},
            'CodeRize': {"CORPID": "CODERIZE15032016", "USERID": "NILESHS", "ACCOUNTNO": "187505000478"},
            'Public Tenant': {"CORPID": "582735465", "USERID": "NILESHSH", "ACCOUNTNO": "346105001227"},
        }

        if client_name in tenant_map:
            variable_data = tenant_map[client_name]
        else:
            raise Exception(f"client_name not found: {client_name}")

        common_data.update(variable_data)
        self.data = common_data


    def get_for_account_statement(self, from_date, to_date):
        
        """ Format the data as needed by account statement API """

        valid_fields = ["AGGRID", "CORPID", "USERID", "URN", "ACCOUNTNO"]

        data = {valid_field: self.data[valid_field]
                for valid_field in valid_fields}

        data["FROMDATE"] = from_date
        data["TODATE"] = to_date
        return data

    def get_for_balance_fetch(self):
        """ Format the data as needed by Balance API """
        
        valid_fields = ["AGGRID", "CORPID", "USERID", "URN", "ACCOUNTNO"]
        data = {valid_field: self.data[valid_field]
                for valid_field in valid_fields}
        return data
