import pandas as pd
import numpy as np
import sipri_info as si
from typing import Set

extra_cols = ["sipri_name", "sipri_alpha", "iso_alpha"]

def create_df(sipri_code, is_import) -> pd.DataFrame:
    """Creates the buyer DataFrame of the given SIPRI entity from corresponding CSV files.
    :param str sipri_code: SIPRI code of chosen country
    :return: Buyer DataFrame
    """
    df = pd.read_csv("data//" + sipri_code + "_buyer.csv", encoding='latin-1', index_col="tidn") if is_import else pd.read_csv("data//" + sipri_code + "_seller.csv", encoding='latin-1', index_col="tidn")
    return df

def perform_db_timelapse_ops(is_import) -> pd.DataFrame:
    """Performs the database "import minus export" operations.
    :return: Map DataFrame for drawing a choropleth map of imports & exports.
    """
    tl_map_df = pd.DataFrame(columns=extra_cols)

    for key, value in si.ENTITY_DICT.items():
        print(key)

        country_df = create_df(value[0], True) if is_import else create_df(value[0], False)

        if not country_df.empty:
            weapons_timelapse_pt = pd.pivot_table(country_df,
                                                  values='nrdel',
                                                  index='odat',
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

    tl_map_df = tl_map_df.fillna(0)

    for x in range(len(tl_map_df.index) - 1):
        if tl_map_df.iloc[x]["sipri_name"] == tl_map_df.iloc[x+1]["sipri_name"]:
            tl_map_df.at[x+1, "All"] += tl_map_df.at[x, "All"]

    #fill in years between with same total
    tl_map_df.astype({'odat': np.int64})

    for key, value in si.ENTITY_DICT.items():
        if key in tl_map_df.values:
            for y in range(int(tl_map_df.loc[tl_map_df['sipri_name'] == key]["odat"].min()), 2021):
                if not ((tl_map_df['sipri_name'] == key) & (tl_map_df['odat'] == y)).any():

                    fill_row = tl_map_df.loc[(tl_map_df["sipri_name"] == key) & (tl_map_df["odat"] == y-1)].copy()
                    fill_row["odat"] = y
                    tl_map_df = tl_map_df.append(fill_row, ignore_index=True)

    file = "data/tl_map_i_df.csv" if is_import else "data/tl_map_e_df.csv"
    tl_map_df_file = open(file, "w")
    tl_map_df.to_csv(path_or_buf=tl_map_df_file, index=False)
    tl_map_df_file.close()

    return tl_map_df

def load_transparency_df(start_year=1992) -> pd.DataFrame:
    """Perform operations on the data we already have to generate a transparency index.
    :param int start_year: Starting year (default 1992)
    :return: DataFrame of transparency scores
    """
    transparency_df = pd.read_csv("Transparency.csv").set_index('ISO Code')
    return transparency_df

def load_stockpiles_df() -> pd.DataFrame:
    """Creates the stockpiles DataFrame of the given SIPRI entity from corresponding CSV files.
        :param str sipri_code: SIPRI code of chosen country
        :return: Stockpiles DataFrame
    """
    stockpile_df = pd.read_csv("Stockpiles.csv").set_index('ISO Code')
    return stockpile_df

def load_tl_map_df(is_import) -> pd.DataFrame:
    """Returns a previously-made tl_map_i_df.csv file.
    :return: Map DataFrame for drawing a timeline choropleth map of imports.
    """
    tl_map_df = pd.read_csv("data/tl_map_i_df.csv") if is_import else pd.read_csv("data/tl_map_e_df.csv")
    return tl_map_df
