"""
Created 2021-06-12 12:49 PM

@author: Victor Mercola
"""

import gen_db
import db_ops
import map_drawing


def prompt(prompt_str) -> bool:
    """ Prompts the user a question that can be answered with yes (y) or no (n); defaults to no.

    :param str prompt_str: String to use as a prompt
    :return: True if yes, False if no
    """
    return input(prompt_str + " ").lower() == "y"


if __name__ == "__main__":

    if prompt("Download Import & Export Tables from SIPRI [y/N]?"):
        gen_db.download_sipri_data()

    if prompt("Recreate SIPRI Database [y/n]?"):
        sipri_df = db_ops.recreate_sipri_db()

    if prompt("Find missing codes [y/N]?"):
        print("Missing codes: " + db_ops.find_missing_codes().__str__())

    if prompt("Perform import & export database operations [y/N]?"):
        ie_map_df = db_ops.perform_db_ie_ops()
    else:
        ie_map_df = db_ops.load_ie_map_df()

    if prompt("Draw import & export choropleth map [y/n]?"):
        map_drawing.draw_ie_map(ie_map_df)

    if prompt("Perform import & export over-time database operations [y/n]?"):
        tl_map_df = db_ops.perform_db_timelapse_ops()
    else:
        tl_map_df = db_ops.load_tl_map_df()

    if prompt("Draw timelapse map [y/n]?"):
        map_drawing.draw_tl_map(tl_map_df)

    if prompt("Perform transparency index operations [y/n]?"):
        transparency_table = db_ops.generate_transparency_index()
    else:
        transparency_table = db_ops.load_transparency_table()

    if prompt("Draw transparency map [y/n]?"):
        map_drawing.draw_transparency_map(transparency_table)

    if prompt("Draw stockpile map [y/n]?"):
        map_drawing.draw_stockpile_map(transparency_table)
    pass
