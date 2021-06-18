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

    # if prompt("Download Import & Export Tables from SIPRI [y/n]?"):
    #     gen_db.download_sipri_data()

    if prompt("Perform import & export over-time database operations [y/n]?"):
        tl_i_map_df = db_ops.perform_db_timelapse_ops(True)
        tl_e_map_df = db_ops.perform_db_timelapse_ops(False)
    else:
        tl_i_map_df = db_ops.load_tl_map_df(True)
        tl_e_map_df = db_ops.load_tl_map_df(False)

    if prompt("Draw timelapse import map [y/n]?"):
        map_drawing.draw_tl_map(tl_i_map_df)

    if prompt("Draw timelapse export map [y/n]?"):
        map_drawing.draw_tl_map(tl_e_map_df)

    if prompt("Draw transparency map [y/n]?"):
        transparency_df = db_ops.load_transparency_df()
        map_drawing.draw_transparency_map(transparency_df)

    if prompt("Draw stockpiles map [y/n]?"):
        stockpiles_df = db_ops.load_stockpiles_df()
        map_drawing.draw_stockpiles_map(stockpiles_df)
