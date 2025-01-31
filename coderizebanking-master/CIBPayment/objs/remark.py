class Remark:

    def __init__(self, remark_string):
        self.remark_string = remark_string

        self.separator = None

        self.remark_main_type = None
        self.remark_subtype = None
        self.remark_account_no = None
        self.remark_IFSC = None
        self.remark_unsplit = None
        self.remark_comment = None
        self.remark_from_bank = None
        self.remark_payer_name = None
        self.remark_upi_address = None

        self.split_df_row = None

    def split_remarks(self):
        """
        Split remark based on various rules written below.
        :return: A Dict with various parameters
        """

        remark = self.remark_string
        try:
            _ = remark[:6].split("/")[1]
            self.separator = "/"
        except IndexError:
            self.separator = "-"

        data = remark.split(self.separator)
        if self.separator == "/":
            if 'INF/NEFT' in remark:
                split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[1], 'remark_account_no': data[2],
                                'remark_IFSC': data[3],
                                'remark_unsplit': data[4:]}
            elif 'INF/INFT' in remark:
                if len(data) == 5:
                    split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[1],
                                    'remark_account_no': data[2],
                                    'remark_comment': data[3], 'remark_payer_name': data[4]}
                elif len(data) == 4:
                    split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[1],
                                    'remark_account_no': data[2],
                                    'remark_payer_name': data[3]}
                else:
                    split_df_row = {'remark_unsplit': data}
            elif 'BIL/INFT' in remark:
                split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[1], 'remark_account_no': data[2],
                                'remark_comment': data[3], 'remark_payer_name': data[4]}

                self.remark_main_type = data[0]
                self.remark_subtype = data[1]
                self.remark_account_no = data[2]
                self.remark_comment = data[3]
                self.remark_payer_name = data[4]

                remark_unsplit = [j for k, j in enumerate(data) if (k > 3 and j != '')]
                if len(remark_unsplit) > 0:
                    split_df_row['remark_unsplit'] = remark_unsplit
                    self.remark_unsplit = str(remark_unsplit)
            elif 'UPI' in remark:
                split_df_row = {'remark_subtype': data[0], 'remark_account_no': data[1], 'remark_comment': data[2],
                                'remark_upi_address': data[3], 'remark_from_bank': data[4]}
                remark_unsplit = [j for k, j in enumerate(data) if (k > 4)]
                if len(remark_unsplit) > 0:
                    split_df_row['remark_unsplit'] = remark_unsplit
            elif 'MMT/IMPS' in remark:
                if len(data) == 6:
                    split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[1],
                                    'remark_account_no': data[2],
                                    'remark_payer_name': data[4], 'remark_from_bank': data[5],
                                    'remark_comment': data[3]}
                elif len(data) == 5:
                    split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[1],
                                    'remark_account_no': data[2],
                                    'remark_payer_name': data[3], 'remark_from_bank': data[4]}
                else:
                    split_df_row = {'remark_unsplit': data}
            elif 'BY CASH' in remark:
                split_df_row = {'remark_unsplit': data}
            elif data[0] == 'CAM':
                split_df_row = {'remark_main_type': data[0], 'remark_subtype': data[2], 'remark_unsplit': data[1:]}
            elif 'RTGS' in remark:
                split_df_row = {'remark_unsplit': data}
            elif 'TRF/' in remark:
                split_df_row = {'remark_unsplit': data}
            elif 'SGST' in remark or 'CGST' in remark:
                split_df_row = {'remark_unsplit': data}
            else:
                split_df_row = {'remark_unsplit': data}

        elif self.separator == "-":
            if data[0] == 'NEFT':
                if len(data) == 4:
                    split_df_row = {'remark_subtype': data[0], 'remark_payer_name': data[2], 'remark_IFSC': data[1],
                                    'remark_comment': data[3],
                                    'remark_unsplit': [j for k, j in enumerate(data) if (k > 3)]}
                elif len(data) == 3:
                    split_df_row = {'remark_subtype': data[0], 'remark_payer_name': data[2], 'remark_IFSC': data[1],
                                    'remark_unsplit': [j for k, j in enumerate(data) if (k > 3)]}
                else:
                    split_df_row = {'remark_unsplit': data}
            elif data[0] == 'RTGS':
                split_df_row = {'remark_subtype': data[0], 'remark_account_no': '', 'remark_comment': data[1],
                                'remark_payer_name': data[2],
                                'remark_unsplit': data[3:]}
            elif 'BY CASH' in remark:
                split_df_row = {'remark_subtype': data[0], 'remark_unsplit': data[1:]}
            else:
                split_df_row = {'remark_unsplit': data}
        else:
            raise Exception("no separator")

        split_df_row['remark'] = remark

        self.split_df_row = split_df_row
        return self.split_df_row


if __name__ == '__main__':

    import pandas

    csv_file = r"E:\CodeRizer_Work\Projects\FruitlyPayments\data\account_statement.xlsx"
    df = pandas.read_excel(csv_file)
    # print(df)

    for row in df.REMARKS:
        a = Remark(remark_string=row).split_remarks()
        print(f"{a} \t\t {row}")
