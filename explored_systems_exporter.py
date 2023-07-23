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

    # Set the format for the right-most column
    format_right_column = workbook.add_format({'bg_color': '#FFFF00'})

    # Set the format for the topmost cell in the right-most column
    format_top_cell = workbook.add_format({'bg_color': '#FFFFFF'})

    for civ in all_civs:

        indexes = np.where(civ.explored_space)

        new_data = [["Short Coords", "q", "r", "Description", "Notes"]]

        for i in range(indexes[0].size):
            # Append the extracted information as a new row in the new_data list

            new_data.append([f"({indexes[0][i]-42}, {indexes[1][i]-42})", indexes[0][i]-42, indexes[1][i]-42,
                             all_systems[(indexes[0][i], indexes[1][i])].description,""])

        new_array = np.array(new_data)

        print(new_array)
        df = pd.DataFrame(new_array)

        writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

        # Write the DataFrame to the Excel sheet
        df.to_excel(writer, index=False, header=False)

    writer.close()
#
# Assume you have a list of DataFrames
dataframes = [df1, df2, df3]  # List of your DataFrames

# Create an Excel writer using pandas

# Iterate over each DataFrame and write to a separate sheet
for i, df in enumerate(dataframes):
    # Write the DataFrame to a sheet
    sheet_name = f'Sheet{i+1}'
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Get the worksheet object
    worksheet = writer.sheets[sheet_name]

    # Set the right-most column to the specific format
    last_column = df.shape[1] - 1
    worksheet.set_column(last_column, last_column, None, format_right_column)

    # Write a blank cell in the topmost cell of the right-most column
    worksheet.write_blank(0, last_column, None, format_top_cell)

# Save the Excel file
writer.save()


if __name__ == "__main__":
    main()
