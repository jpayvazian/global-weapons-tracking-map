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

    if prompt("Download Import & Export Tables from SIPRI [y/n]?"):
        gen_db.download_sipri_data()

    if prompt("Perform import & export database operations [y/n]?"):
        i_map_df = db_ops.perform_db_i_ops()
        e_map_df = db_ops.perform_db_e_ops()

    else:
        i_map_df = db_ops.load_i_map_df()
        e_map_df = db_ops.load_e_map_df()

    if prompt("Draw import & export choropleth map [y/n]?"):
        map_drawing.draw_ie_map(e_map_df)

    # if prompt("Perform import & export over-time database operations [y/n]?"):
    #     tl_map_df = db_ops.perform_db_timelapse_ops()
    # else:
    #     tl_map_df = db_ops.load_tl_map_df()

    # if prompt("Draw timelapse map [y/n]?"):
    #     map_drawing.draw_tl_map(tl_map_df)
    #
    # if prompt("Perform transparency index operations [y/n]?"):
    #     db_ops.create_transparency_dfs()
    #
    # if prompt("Draw transparency map [y/n]?"):
    #     map_drawing.draw_transparency_map(transparency_df)
    pass