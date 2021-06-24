"""
@file gen_db.py

The functions in this file are used for downloading data from OSINT databases.

@author Victor Mercola
@author Benjamin Lunden
@author Jack Ayvazian
"""

import os
import shutil
import sipri
import sipri_info as si


def download_sipri_data():
    """
    Downloads import & export data for each country from SIPRI's Arms Transfer Database, then stores them in CSV files
    under the "data" folder.

    :return: None
    """

    try:
        # Try to create the "data" file locally
        os.mkdir("data")
        print("\"data\" folder created")
    except FileExistsError:
        # If that folder already exists, wipe it & remake it
        print("\"data\" folder already exists; deleting & remaking")
        if os.path.exists("data"):
            shutil.rmtree("data")
        os.mkdir("data")

    # The third-party sipri library performs queries on SIPRI's Arms Transfer Database automatically.
    # If the query has results, they are returned as a CSV string that can be written as a file.
    # If the query has no results, an HTML file is returned instead.
    # An empty CSV header replaces the HTML file to signify an empty dataset.

    for key, value in si.ENTITY_DICT.items():
        print(key)

        # Download & save seller data for each country

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

        # Download & save buyer data for each country

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
