import os
import pandas as pd

dataframes = []
output_folder = r"C:\python\scripts\pdfeditor2\processing\downloads"

# Iterate over each file in the output folder
for file_name in os.listdir(output_folder):
    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        file_path = os.path.join(output_folder, file_name)

        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Add the "Object ID" field from the file name (minus the extension)
        object_id = os.path.splitext(file_name)[0]
        df["Object ID"] = object_id

        # Append the DataFrame to the list
        dataframes.append(df)

# Combine all DataFrames, keeping all fields and adding new ones as encountered
combined_df = pd.concat(dataframes, ignore_index=True, sort=False)

# Save the combined DataFrame to a new Excel file
combined_output_path = r"C:\python\scripts\pdfeditor2\processing\combined_output2.xlsx"
combined_df.to_excel(combined_output_path, index=False)

update_csv = combined_output_path.split(".")[0] + ".csv"

print(f"All tables have been combined and saved to {combined_output_path}")


def excel2csvProcess(combined_output_path):
    combined_df = pd.read_excel(combined_output_path)
    field_names_list = [name.replace("-", "_") for name in combined_df.columns.tolist()]
    print(field_names_list)

    update_csv = combined_output_path.split(".")[0] + ".csv"

    combined_df.to_csv(update_csv, index=False)

    df = pd.read_csv(update_csv)
    remove_vowels = lambda text: "".join(
        char for char in text if char.lower() not in "aeiou"
    )
    field_names = [
        remove_vowels(name) if len(name) > 13 else name for name in field_names_list
    ]
    def remove_vowels(text):
        return "".join(char for char in text if char.lower() not in "aeiou")

    # Assign the new field names to the DataFrame
    df.columns = field_names

    # Optionally, write the modified DataFrame to a new CSV file
    df.to_csv(update_csv, index=False)

excel2csvProcess(combined_output_path)



def update_table(combined_output, recent_output):
    df = pd.read_csv(combined_output)
    df_update = pd.read_csv(recent_output)

    dfs = [df, df_update]

    df_combined = pd.concat(dfs, ignore_index=True, sort=False)

    df_combined.to_csv(combined_output, index=False)

    print(f"{combined_output} table updated with data from {recent_output}")

update_table(r"C:\python\scripts\pdfeditor2\processing\combined_output.csv", update_csv)