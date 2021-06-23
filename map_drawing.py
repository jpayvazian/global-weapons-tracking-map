import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import sipri_info as si

LAND_COLOR = "#dddddd"


def draw_tl_map(tl_map_df, is_import):
    """
    Draws the "imports and exports over time" map using Plotly.

    :param pd.DataFrame tl_map_df: Map DataFrame for drawing choropleth map over time.
    :param boolean is_import: True is data is imports, False if exports
    :return: None, but creates HTML file
    """

    tl_map_df = tl_map_df.sort_values(by="odat")

    if is_import:
        title = "Imports"
        color = "dense"
    else:
        title = "Exports"
        color = "amp"

    fig = px.choropleth(tl_map_df,
                        locations="iso_alpha",
                        hover_name="sipri_name",
                        color="All",
                        range_color=[tl_map_df["All"].min(), tl_map_df["All"].max()],
                        animation_group="sipri_name",
                        animation_frame="odat",
                        hover_data=si.WCATS_DICT.keys(),
                        labels=dict(si.WCATS_DICT, **{"odat": "Year", "All": "Total"}),
                        title="Major Conventional Weapon " + title + " over time from SIPRI",
                        color_continuous_scale=color,
                        projection="robinson")

    fig.update_geos(landcolor=LAND_COLOR)

    plot(fig)


def draw_transparency_map(transparency_df):
    """
    Draws the "Transparency indicator" map using Plotly.

    :param pd.DataFrame transparency_df: Map DataFrame for drawing choropleth map.
    :return: None, but creates HTML file
    """
    fig = px.choropleth(transparency_df,
                        locations=transparency_df.index,
                        hover_name="name",
                        color="Total Reports",
                        hover_data=['Exports/Imports', 'Military Holdings', 'National Production', 'SALW'],
                        title="Transparency Indicator: Number of voluntary UNROCA weapon reports 1992-2020",
                        color_continuous_scale="algae",
                        projection="robinson")

    fig.update_geos(landcolor=LAND_COLOR)

    plot(fig)


def draw_stockpiles_map(stockpiles_df):
    """
    Draws the "Stockpiles" map using Plotly.

    :param pd.DataFrame stockpiles_df: Map DataFrame for drawing choropleth map.
    :return: None, but creates HTML file
    """
    fig = px.choropleth(stockpiles_df,
                        locations=stockpiles_df.index,
                        hover_name="name",
                        color="Stockpiles",
                        hover_data=['Year', 'Tanks', 'Combat vehicles', 'Artillery', 'Aircraft', 'Helicopters',
                                    'Warships', 'Missiles/Missile launchers', 'Stockpiles'],
                        title="Major Conventional Weapon Stockpiles from UNROCA",
                        color_continuous_scale="Burg",
                        projection="robinson")

    fig.update_geos(landcolor=LAND_COLOR)

    plot(fig)


def draw_combined_ie_map(tl_i_map_df, tl_e_map_df):
    """
    Draws a combined version of the imports & exports map over time.

    :param pd.DataFrame tl_i_map_df: DataFrame for Imports
    :param pd.DataFrame tl_e_map_df: DataFrame for Exports
    :return: none, but creates HTML file
    """

    tl_i_map_df = tl_i_map_df.astype({'odat': np.int64}).sort_values(by="odat")
    tl_e_map_df = tl_e_map_df.astype({'odat': np.int64}).sort_values(by="odat")

    tl_i_map_df["isImport"] = True
    tl_e_map_df["isImport"] = False

    combined_tl_map_df = tl_i_map_df.append(tl_e_map_df, ignore_index=True)

    fig = px.choropleth(combined_tl_map_df,
                        locations="iso_alpha",
                        hover_name="sipri_name",
                        color="All",
                        animation_group="sipri_name",
                        animation_frame="odat",
                        range_color=[combined_tl_map_df["All"].min(), combined_tl_map_df["All"].max()],
                        hover_data=si.WCATS_DICT.keys(),
                        labels=dict(si.WCATS_DICT, **{"odat": "Year", "All": "Total"}),
                        title="Test",
                        facet_col="isImport",
                        # color_continuous_scale=color,
                        projection="robinson")

    # fig.update_geos(landcolor=LAND_COLOR)

    plot(fig)
