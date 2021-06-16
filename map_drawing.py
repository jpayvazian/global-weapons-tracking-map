import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot
import sipri_info as si


def draw_ie_map(ie_map_df):
    """Draws the "imports/exports" map using Plotly.
    :param pd.DataFrame ie_map_df: Map DataFrame for drawing choropleth map.
    :return: None, but creates HTML file
    """
    fig2 = px.choropleth(ie_map_df,
                         locations="iso_alpha",
                         hover_name="sipri_name",
                         color="All",
                         hover_data=si.WCATS_DICT.keys(),
                         labels=dict(si.WCATS_DICT, **{"All": "total"}),
                         projection="robinson")
    plot(fig2)

# def draw_tl_map(tl_map_df):
#     """Draws the "imports minus exports over time" map using Plotly.
#     :param pd.DataFrame tl_map_df: Map DataFrame for drawing choropleth map over time.
#     :return: None, but creates HTML file
#     """
#     # tl_map_copy = tl_map_df.copy()
#     #
#     # for row_tuple in tl_map_copy.itertuples():
#     #     if row_tuple.odat == "All":
#     #         tl_map_copy.at[row_tuple.Index, "odat"] = 9999
#     #     else:
#     #         tl_map_copy.at[row_tuple.Index, "odat"] = int(float(tl_map_copy.at[row_tuple.Index, "odat"]))
#     #
#     # tl_map_copy = tl_map_copy.sort_values(by='odat')
#
#     tl_map_df.astype({'odat': np.int64})
#     tl_map_df = tl_map_df.sort_values(by="odat")
#
#     fig = px.choropleth(tl_map_df,
#                         locations="iso_alpha",
#                         hover_name="sipri_name",
#                         color="All",
#                         range_color=[tl_map_df["All"].min(), tl_map_df["All"].max()],
#                         color_continuous_midpoint=0,
#                         animation_group="sipri_name",
#                         animation_frame="odat",
#                         hover_data=si.WCATS_DICT.keys(),
#                         labels=dict(si.WCATS_DICT, **{"odat": "Order Date", "All": "total"}),
#                         title="Munition Imports minus Exports over Time",
#                         projection="robinson")
#
#     plot(fig)

# def draw_transparency_map(transparency_table):
#
#     fig = px.choropleth(transparency_table,
#                         locations=transparency_table.index,
#                         hover_name="sipri_name",
#                         color="Total",
#                         projection="robinson")
#
#     plot(fig)