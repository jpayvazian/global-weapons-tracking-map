import numpy as np
import pandas as pd

import sipri_info as si

EXTRA_COLS = ["sipri_name", "sipri_alpha", "iso_alpha"]
"""
Important extra columns used for processing data for each country.
"""


def create_df(sipri_code, is_import) -> pd.DataFrame:
    """
    Creates the buyer/seller DataFrame of the given SIPRI entity from corresponding CSV files.

    :param str sipri_code: SIPRI code of chosen country
    :param boolean is_import: True if data is imports, False if exports
    :return: DataFrame for buyer or seller
    """
    if is_import:
        df = pd.read_csv("data//" + sipri_code + "_buyer.csv", encoding='latin-1', index_col="tidn")
    else:
        df = pd.read_csv("data//" + sipri_code + "_seller.csv", encoding='latin-1', index_col="tidn")
    return df


def perform_db_timelapse_ops(is_import) -> pd.DataFrame:
    """
    Performs the database operations to accumulate imports/exports over time.

    :param boolean is_import: True if data is imports, False if exports
    :return: Map DataFrame for drawing a choropleth map of imports & exports.
    """

    # Create returning DataFrame
    tl_map_df = pd.DataFrame(columns=EXTRA_COLS)

    # Iterate across all countries
    for key, value in si.ENTITY_DICT.items():
        print(key)

        # Create the corresponding import/export DataFrame for this country
        country_df = create_df(value[0], True) if is_import else create_df(value[0], False)

        if not country_df.empty:

            # Show how many delivered weapons of each category were sold/bought by this country for every year
            weapons_timelapse_pt = pd.pivot_table(country_df,
                                                  values='nrdel',
                                                  index='odat',
                                                  columns='wcat',
                                                  aggfunc=np.sum,
                                                  margins=True,  # creates the "All" row and column
                                                  fill_value=0)

            # Fill NaNs
            weapons_timelapse_pt.fillna(0, inplace=True)
            weapons_timelapse_pt.drop("All", inplace=True)  # Does not drop everything, just one of the margins
            weapons_timelapse_pt.reset_index(inplace=True)

            # TODO: Optimize this code! When adding rows to the tl_map_df DataFrame, perform operations here instead
            #  to calculate the cumulative sums by year.

            # Populate the rows of tl_map_df
            for pt_row in weapons_timelapse_pt.iterrows():
                # Create a new row with this country's information
                new_row = pd.Series({'sipri_name': key,
                                     'sipri_alpha': value[0],
                                     'iso_alpha': value[1],
                                     'odat': pt_row[1]["odat"]})

                new_row_data = np.sum(
                    weapons_timelapse_pt[weapons_timelapse_pt["odat"] <= pt_row[1]["odat"]].drop(["odat"], axis=1))

                new_row = new_row.append(new_row_data)
                tl_map_df = tl_map_df.append(new_row, ignore_index=True)

            for year in range(weapons_timelapse_pt["odat"].min(), weapons_timelapse_pt["odat"].max()):
                if not (year in weapons_timelapse_pt["odat"].to_list()):
                    previous_year_data = tl_map_df[(tl_map_df["iso_alpha"] == "AFG") & (tl_map_df["odat"] == (year - 1))]
                    previous_year_data.assign(odat=year)
                    tl_map_df = tl_map_df.append(previous_year_data, ignore_index=True)

    tl_map_df = tl_map_df.fillna(0)

    file = "data/tl_map_i_df.csv" if is_import else "data/tl_map_e_df.csv"
    tl_map_df_file = open(file, "w")
    tl_map_df.to_csv(path_or_buf=tl_map_df_file, index=False)
    tl_map_df_file.close()

    return tl_map_df


def load_transparency_df() -> pd.DataFrame:
    """
    Loads transparency data CSV file.

    :return: DataFrame of transparency scores
    """
    transparency_df = pd.read_csv("Transparency.csv").set_index('ISO Code')
    return transparency_df


def load_stockpiles_df() -> pd.DataFrame:
    """
    Loads stockpiles data CSV file.

    :return: Stockpiles DataFrame
    """
    stockpile_df = pd.read_csv("Stockpiles.csv").set_index('ISO Code')
    return stockpile_df


def load_tl_map_df(is_import) -> pd.DataFrame:
    """
    Loads previously-made tl_map_df.csv file.

    :param boolean is_import: True if data is imports, False if exports
    :return: Map DataFrame for drawing a timeline choropleth map of imports/exports.
    """
    tl_map_df = pd.read_csv("data/tl_map_i_df.csv") if is_import else pd.read_csv("data/tl_map_e_df.csv")
    return tl_map_df
