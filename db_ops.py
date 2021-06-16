"""
Created 2021-06-12 12:58 PM

@author: Victor Mercola
"""

import pandas as pd
import numpy as np

import sipri_info as si
from typing import Set

extra_cols = ["sipri_name", "sipri_alpha", "iso_alpha"]


def find_missing_codes() -> Set[str]:
    """Returns the missing SIPRI codes in the CSV files of the database.

    :return: Set of
    """

    missing_sipri_codes = set()

    for key, value in si.ENTITY_DICT.items():

        # Check if there are any missing entities in our list
        code_set = set()

        buyer_df, seller_df = create_buyer_seller_dfs(value[0])

        code_set.update(buyer_df.sellercod.tolist())
        code_set.update(seller_df.buyercod.tolist())

        for code in code_set:
            if not (code in si.SIPRI_CODES):
                # print("Code " + code + " not found in SIPRI_CODES")
                missing_sipri_codes.add(code)

    return missing_sipri_codes


def create_buyer_seller_dfs(sipri_code) -> [pd.DataFrame, pd.DataFrame]:
    """Creates the buyer and seller DataFrames of the given SIPRI entity from corresponding CSV files.

    :param str sipri_code: SIPRI code of chosen country
    :return: Buyer DataFrame, Seller DataFrame
    """

    buyer_df = pd.read_csv("data//" + sipri_code + "_buyer.csv", encoding='latin-1', index_col="tidn")
    seller_df = pd.read_csv("data//" + sipri_code + "_seller.csv", encoding='latin-1', index_col="tidn")

    return buyer_df, seller_df


def create_country_df(sipri_code, add_custom_columns=False) -> pd.DataFrame:
    """Creates a DataFrame that contains all information about a specific country.

    This does not add the "isImport" and "munitionTally" columns.

    :param str sipri_code: SIPRI code of the specified entity
    :param add_custom_columns: include custom columns ("isImport", "munitionTally") for the DataFrame
    :return: DataFrame for a SIPRI entity
    """
    # Create buyer & seller dataframes
    buyer_df, seller_df = create_buyer_seller_dfs(sipri_code)

    # Concatenate Seller & Buyer DataFrames
    country_df = pd.concat([seller_df, buyer_df])

    if add_custom_columns is True:
        # Insert "isImport" and "munitionTally" rows with all "None" values
        country_df.insert(2, "isImport", None, allow_duplicates=True)
        country_df.insert(14, "munitionTally", None, allow_duplicates=True)

        # Note: "nrdel" = number delivered, and "ornum" = order numbered

        # Populate values of isImport and munitionTally rows
        # "isImport" is true if the trade is an import, and false otherwise.
        # "munitionTally" = nrdel if isImport is true, -1 * nrdel otherwise.
        for trade in country_df.itertuples():

            # For imports, the country code is equal to the buyer code.
            if trade.buyercod.__eq__(sipri_code):
                country_df.at[trade.Index, "isImport"] = True
                country_df.at[trade.Index, "munitionTally"] = 1 * trade.nrdel

            # For exports, the country code is equal to the seller code.
            elif trade.sellercod.__eq__(sipri_code):
                country_df.at[trade.Index, "isImport"] = False
                country_df.at[trade.Index, "munitionTally"] = -1 * trade.nrdel

            # If the country is in neither, something is wrong.
            else:
                raise Exception(
                    "Error in populating isImport and munitionTally rows")

    return country_df


def perform_db_timelapse_ops() -> pd.DataFrame:
    """Performs the database "import minus export" operations.

    :return: Map DataFrame for drawing a choropleth map of imports & exports.
    """

    tl_map_df = pd.DataFrame(columns=extra_cols)

    for key, value in si.ENTITY_DICT.items():
        print(key)

        country_df = create_country_df(value[0], add_custom_columns=True)

        weapons_timelapse_pt = pd.pivot_table(country_df,
                                              values='munitionTally',
                                              index=['odat'],
                                              columns='wcat',
                                              aggfunc=np.sum,
                                              margins=True,
                                              fill_value=0)

        weapons_timelapse_pt = weapons_timelapse_pt.fillna(0)

        for pt_row in weapons_timelapse_pt.iterrows():
            new_row = pd.Series({'sipri_name': key,
                                 'sipri_alpha': value[0],
                                 'iso_alpha': value[1],
                                 'odat': pt_row[0]})
            new_row = new_row.append(pt_row[1])
            if new_row["odat"] != "All":
                tl_map_df = tl_map_df.append(new_row, ignore_index=True)
            # tl_map_df = tl_map_df.append(new_row, ignore_index=True)

    tl_map_df = tl_map_df.fillna(0)
    tl_map_df_file = open("data/tl_map_df.csv", "w")
    tl_map_df.to_csv(path_or_buf=tl_map_df_file, index=False)
    tl_map_df_file.close()

    return tl_map_df


def perform_db_ie_ops() -> pd.DataFrame:
    """Performs the database "import minus export" operations.

    :return: Map DataFrame for drawing a choropleth map of imports & exports.
    """

    ie_map_df = pd.DataFrame(columns=extra_cols)

    for key, value in si.ENTITY_DICT.items():
        print(key)

        country_df = create_country_df(value[0], add_custom_columns=True)
        weapons_pt = pd.pivot_table(country_df,
                                    values='munitionTally',
                                    index='wcat',
                                    aggfunc=np.sum,
                                    margins=True,
                                    fill_value=0)
        new_row = pd.Series({'sipri_name': key,
                             'sipri_alpha': value[0],
                             'iso_alpha': value[1]})
        new_row = new_row.append(weapons_pt["munitionTally"])
        ie_map_df = ie_map_df.append(new_row, ignore_index=True)

        # # Weapons dictionary: desig2 -> [wcat, desc, total]
        # weapons_dict = {}
        #
        # # Populate weapons_dict based on the desig2 values in each line
        # for trade in country_df.itertuples():
        #
        #     # Make sure "nan" rows are ignored
        #     if not math.isnan(trade.nrdel):
        #         if trade.desig2 not in weapons_dict.keys():
        #             weapons_dict[trade.desig2] = {"wcat": trade.wcat,
        #                                           "desc": trade.desc,
        #                                           "total": trade.munitionTally}
        #         else:
        #             weapons_dict[trade.desig2]["total"] += trade.munitionTally
        #
        # # convert dictionary to dataFrame
        # weapons_df = pd.DataFrame(columns=['desig2', 'wcat', 'desc', 'total'])
        #
        # for wkey, wvalue in weapons_dict.items():
        #     weapons_df = weapons_df.append({"desig2": wkey,
        #                                     "wcat": wvalue["wcat"],
        #                                     "desc": wvalue["desc"],
        #                                     "total": wvalue["total"]},
        #                                    ignore_index=True)
        #
        # # Pivot table of weapons by category
        # weapons_pt = pd.pivot_table(weapons_df,
        #                             values='total',
        #                             index=['wcat'],
        #                             aggfunc=np.sum)
        #
        # # Append to ie_map_df
        # weapons_pt_dict = weapons_pt.to_dict()['total']
        # for wcat in si.WCATS:
        #     # Make sure each weapons category is represented; otherwise, there
        #     # will be NaNs where there should be 0's
        #     if wcat not in weapons_pt_dict.keys():
        #         weapons_pt_dict.update({wcat: 0})
        # weapons_pt_dict.update({'sipri_name': key,
        #                         'sipri_alpha': value[0],
        #                         'iso_alpha': value[1],
        #                         'All': sum(weapons_pt.total)})
        # ie_map_df = ie_map_df.append(weapons_pt_dict, ignore_index=True)

    ie_map_df = ie_map_df.fillna(0)
    ie_map_df_file = open("data/ie_map_df.csv", "w")
    ie_map_df.to_csv(path_or_buf=ie_map_df_file, index=False)
    ie_map_df_file.close()

    return ie_map_df


def recreate_sipri_db() -> pd.DataFrame:
    """Recreates the entire SIPRI database that has been downloaded.

    :return:
    """

    sipri_df = pd.DataFrame()

    for key, value in si.ENTITY_DICT.items():
        country_df = create_country_df(value[0])

        sipri_df = sipri_df.append(country_df)

    sipri_df = sipri_df.drop_duplicates().sort_index()
    return sipri_df


def load_ie_map_df() -> pd.DataFrame:
    """Returns a previously-made ie_map_df.csv file.

    :return: Map DataFrame for drawing a choropleth map of imports & exports.
    """
    return pd.read_csv("data/ie_map_df.csv")


def load_tl_map_df() -> pd.DataFrame:
    """Returns a previously-made tl_map_df.csv file.

    :return: Map DataFrame for drawing a timeline choropleth map of imports & exports.
    """
    return pd.read_csv("data/tl_map_df.csv")


def generate_transparency_index(start_year=1992) -> pd.DataFrame:
    """Perform operations on the data we already have to generate a transparency index.

    :param int start_year: Starting year (default 1992)
    :return: DataFrame of transparency scores
    """

    transparency_table = pd.DataFrame(columns=extra_cols)

    for key, value in si.ENTITY_DICT.items():

        if value[1] != "":

            country_series = pd.Series({'sipri_name': key,
                                        'sipri_alpha': value[0],
                                        'iso_alpha': value[1]})

            print(key)

            country_df = create_country_df(value[0])
            country_df = country_df[country_df['odat'] >= 1992]

            records = country_df.shape[0]
            country_series = country_series.append(pd.Series({'sipri_records': records,
                                                              'order_date_estimates': country_df['odai'].count(),
                                                              'onum_nans': records - country_df['onum'].count(),
                                                              'order_number_estimates': country_df['onai'].count(),
                                                              'term_nans': records - country_df['term'].count(),
                                                              'coprod_nans': records - country_df['coprod'].count(),
                                                              'nrdel_nans': records - country_df['nrdel'].count(),
                                                              'number_delivered_estimates': country_df['nrdelai'].count(),
                                                              'delyears_nans': records - country_df['delyears'].count()}))
            # print(country_series)
            # "order date is estimate" = odai

            transparency_table = transparency_table.append(country_series, ignore_index=True)

    # Set keys of both tables to the ISO codes
    transparency_table = transparency_table.set_index('iso_alpha')
    unroca_table = pd.read_csv("UNROCA Countries Stockpiles.csv").set_index('ISO Code')

    # Join together
    transparency_table = transparency_table.join(unroca_table)

    # Remove dashes where there should be NaNs
    transparency_table = transparency_table.replace("-", np.nan)

    transparency_table_file = open("data/transparency_table.csv", "w")
    transparency_table.to_csv(path_or_buf=transparency_table_file, index=True)
    transparency_table_file.close()

    return transparency_table

def load_transparency_table() -> pd.DataFrame:
    """Returns a previously-made transparency_table.csv file.

    :return: transparency_table
    """
    return pd.read_csv("data/transparency_table.csv")
