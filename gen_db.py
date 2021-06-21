import os
import shutil
import sipri
import sipri_info as si


def download_sipri_data():
    """
    Downloads SIPRI import and export data by country and stores them in CSV files under "data".
    :return: None
    """
    try:
        os.mkdir("data")
        print("\"data\" folder created")
    except FileExistsError:
        print("\"data\" folder already exists; deleting & remaking")
        if os.path.exists("data"):
            shutil.rmtree("data")
        os.mkdir("data")

    for key, value in si.ENTITY_DICT.items():
        print(key)

        seller_str = sipri.sipri_data(low_year='1950',
                                      high_year='2020',
                                      seller=value[0],
                                      filetype='csv')

        seller_csv = open("data/" + value[0] + "_seller.csv", "w")
        if not seller_str.startswith("<!DOCTYPE"):
            seller_csv.write(seller_str)
            seller_csv.close()
        else:
            seller_csv.write(si.CSV_HEADER)
            seller_csv.close()

        buyer_str = sipri.sipri_data(low_year='1950',
                                     high_year='2020',
                                     buyer=value[0],
                                     filetype='csv')

        buyer_csv = open("data/" + value[0] + "_buyer.csv", "w")
        if not buyer_str.startswith("<!DOCTYPE"):
            buyer_csv.write(buyer_str)
            buyer_csv.close()
        else:
            buyer_csv.write(si.CSV_HEADER)
            buyer_csv.close()
