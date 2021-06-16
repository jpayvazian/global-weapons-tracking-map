import pandas as pd
import numpy as np
import sipri_info as si
from typing import Set

extra_cols = ["sipri_name", "sipri_alpha", "iso_alpha"]

def create_buyer_dfs(sipri_code) -> pd.DataFrame:
    """Creates the buyer DataFrame of the given SIPRI entity from corresponding CSV files.
    :param str sipri_code: SIPRI code of chosen country
    :return: Buyer DataFrame
    """
    buyer_df = pd.read_csv("data//" + sipri_code + "_buyer.csv", encoding='latin-1', index_col="tidn")
    return buyer_df

def create_seller_dfs(sipri_code) -> pd.DataFrame:
    """Creates the seller DataFrame of the given SIPRI entity from corresponding CSV files.
    :param str sipri_code: SIPRI code of chosen country
    :return: Seller DataFrame
    """
    seller_df = pd.read_csv("data//" + sipri_code + "_seller.csv", encoding='latin-1', index_col="tidn")
    return seller_df

def create_transparency_dfs(start_year=1992) -> pd.DataFrame:
    """Perform operations on the data we already have to generate a transparency index.
    :param int start_year: Starting year (default 1992)
    :return: DataFrame of transparency scores
    """
    transparency_df = pd.read_csv("Transparency.csv").set_index('ISO Code')
    return transparency_df

def create_stockpiles_dfs(sipri_code) -> pd.DataFrame:
    """Creates the stockpiles DataFrame of the given SIPRI entity from corresponding CSV files.
        :param str sipri_code: SIPRI code of chosen country
        :return: Stockpiles DataFrame
    """
    stockpile_df = pd.read_csv("Stockpiles.csv").set_index('ISO Code')
    return stockpile_df

def perform_db_i_ops() -> pd.DataFrame:
    """Performs the database operations for imports/exports map.
    :return: Map DataFrame for drawing a choropleth map of imports.
    """
    i_map_df = pd.DataFrame(columns=extra_cols)
    for key, value in si.ENTITY_DICT.items():
        print(key)

        country_df = create_buyer_dfs(value[0])
        weapons_pt = pd.pivot_table(country_df,
                                    values='nrdel',
                                    index='wcat',
                                    aggfunc=np.sum,
                                    margins=True,
                                    fill_value=0)
        new_row = pd.Series({'sipri_name': key,
                             'sipri_alpha': value[0],
                             'iso_alpha': value[1]})

        new_row = new_row.append(weapons_pt["nrdel"])
        i_map_df = i_map_df.append(new_row, ignore_index=True)

    i_map_df = i_map_df.fillna(0)
    i_map_df_file = open("data/i_map_df.csv", "w")
    i_map_df.to_csv(path_or_buf=i_map_df_file, index=False)
    i_map_df_file.close()

    return i_map_df

def perform_db_e_ops() -> pd.DataFrame:
    """Performs the database operations for imports/exports map.
    :return: Map DataFrame for drawing a choropleth map of exports.
    """
    e_map_df = pd.DataFrame(columns=extra_cols)
    for key, value in si.ENTITY_DICT.items():
        print(key)

        country_df = create_seller_dfs(value[0])
        weapons_pt = pd.pivot_table(country_df,
                                    values='nrdel',
                                    index='wcat',
                                    aggfunc=np.sum,
                                    margins=True,
                                    fill_value=0)
        new_row = pd.Series({'sipri_name': key,
                             'sipri_alpha': value[0],
                             'iso_alpha': value[1]})

        new_row = new_row.append(weapons_pt["nrdel"])
        e_map_df = e_map_df.append(new_row, ignore_index=True)

    e_map_df = e_map_df.fillna(0)
    e_map_df_file = open("data/e_map_df.csv", "w")
    e_map_df.to_csv(path_or_buf=e_map_df_file, index=False)
    e_map_df_file.close()

    return e_map_df

# def perform_db_timelapse_ops() -> pd.DataFrame:
#     """Performs the database "import minus export" operations.
#     :return: Map DataFrame for drawing a choropleth map of imports & exports.
#     """
#     tl_map_df = pd.DataFrame(columns=extra_cols)
#
#     for key, value in si.ENTITY_DICT.items():
#         print(key)
#
#         country_df = create_country_df(value[0], add_custom_columns=True)
#
#         weapons_timelapse_pt = pd.pivot_table(country_df,
#                                               values='munitionTally',
#                                               index=['odat'],
#                                               columns='wcat',
#                                               aggfunc=np.sum,
#                                               margins=True,
#                                               fill_value=0)
#
#         weapons_timelapse_pt = weapons_timelapse_pt.fillna(0)
#
#         for pt_row in weapons_timelapse_pt.iterrows():
#             new_row = pd.Series({'sipri_name': key,
#                                  'sipri_alpha': value[0],
#                                  'iso_alpha': value[1],
#                                  'odat': pt_row[0]})
#             new_row = new_row.append(pt_row[1])
#             if new_row["odat"] != "All":
#                 tl_map_df = tl_map_df.append(new_row, ignore_index=True)
#             # tl_map_df = tl_map_df.append(new_row, ignore_index=True)
#
#     tl_map_df = tl_map_df.fillna(0)
#     tl_map_df_file = open("data/tl_map_df.csv", "w")
#     tl_map_df.to_csv(path_or_buf=tl_map_df_file, index=False)
#     tl_map_df_file.close()
#
#     return tl_map_df

def load_i_map_df() -> pd.DataFrame:
    """Returns a previously-made i_map_df.csv file.
    :return: Map DataFrame for drawing a choropleth map of imports.
    """
    return pd.read_csv("data/i_map_df.csv")

def load_e_map_df() -> pd.DataFrame:
    """Returns a previously-made e_map_df.csv file.
    :return: Map DataFrame for drawing a choropleth map of exports.
    """
    return pd.read_csv("data/e_map_df.csv")

def load_tl_map_df() -> pd.DataFrame:
    """Returns a previously-made tl_map_df.csv file.
    :return: Map DataFrame for drawing a timeline choropleth map of imports & exports.
    """
    return pd.read_csv("data/tl_map_df.csv")


