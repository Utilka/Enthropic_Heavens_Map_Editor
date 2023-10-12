import numpy as np
import pandas as pd
from Player_DB_handler import *
from System_DB_handler import *
import xlsxwriter


# Create a 2D NumPy array of strings
def main():
    all_civs = load_civs()
    all_systems = load_systems()

    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

    # Get the xlsxwriter workbook object
    workbook = writer.book

    format_stel_bod_column = workbook.add_format({'font_size': 8, "font":"JetBrains Mono"})

    format_stel_bod_column_header = workbook.add_format({'font_size': 11})

    for civ in all_civs:

        indexes = np.where(civ.explored_space)

        new_data = [["Short Coords", "q", "r", "Short Description", "Stellar Bodies Description"]]

        for i in range(indexes[0].size):
            # Append the extracted information as a new row in the new_data list

            new_data.append([f"({indexes[0][i] - 42}, {indexes[1][i] - 42})", indexes[0][i] - 42, indexes[1][i] - 42,
                             all_systems[(indexes[0][i], indexes[1][i])].short_description,
                             all_systems[(indexes[0][i], indexes[1][i])].stellar_bod_description])

        new_array = np.array(new_data)

        df = pd.DataFrame(new_array)

        sheet_name = f'Sheet{civ.player_id}'
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

        # Get the worksheet object
        worksheet = writer.sheets[sheet_name]

        # Set the right-most column to the specific format
        last_column = df.shape[1] - 1
        worksheet.set_column(last_column, last_column, None, format_stel_bod_column)
        # Write a blank cell in the topmost cell of the right-most column
        worksheet.write(0, last_column, "Stellar Bodies Description", format_stel_bod_column_header)
        worksheet.autofit()

    writer.close()


if __name__ == "__main__":
    main()
