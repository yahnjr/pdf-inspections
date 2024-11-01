import os
import pandas as pd
from pdfrw import PdfReader, PdfWriter, PdfDict

# Create extra data columns for use in dashboards
df = pd.read_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output.csv")

df["fail_count"] = df.apply(lambda row: (row == "fail").sum(), axis=1)

df["intersection_name"] = df.apply(
    lambda row: f"{row['ns_road']} & {row['ew_road']}", axis=1
)

df["file_link"] = df.apply(
    lambda row: f"O:\\City of North Plains\\City Projects\\Misc\\ADA Study\\GIS\\Outputs\\{row['fileName']}.pdf",
    axis=1,
)

df["failing_test"] = "none"

for index, row in df.iterrows():
    failing_tests = []
    for col in df.columns:
        if row[col] == "fail":
            failing_tests.append(col)

    if failing_tests:
        df.at[index, "failing_test"] = ", ".join(failing_tests)

df["failing_test"] = df["failing_test"].apply(
    lambda x: x.replace("none, ", "") if x.startswith("none, ") else x
)

df.to_csv(
    r"C:\python\scripts\pdfeditor2\processing\combined_processed_output.csv",
    index=False,
)

print(df)

import os

folder_path = r"C:\python\scripts\transferPDFS"

for filename in os.listdir(folder_path):
    if filename.endswith("_red.pdf"):
        new_filename = filename.replace("_red", "")
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        os.rename(old_file, new_file)

        print(f"{old_file} renamed to {new_file}")

print("Files have been renamed successfully!")



# For double checking and fixing comment fields. Some pdfs don't work due to corruption, so need to exclude them. 
def update_comments_in_pdf(input_pdf_path, comments, output_folder):
    input_pdf = PdfReader(input_pdf_path)

    for page in input_pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                field = annotation.get("/T")
                if field and (field == "(ADA2_COMNT)" or field == "(ADA_COMNT)"):
                    annotation.update(PdfDict(V=comments, AP=PdfDict()))
                    print(f"\nComments field updated with: \n{comments}")
                    break 

    output_path = os.path.join(output_folder, os.path.basename(input_pdf_path))
    PdfWriter().write(output_path, input_pdf)
    print(f"Saved updated PDF to {output_path}")

def loop_folder_comments(input_folder, csv_path, output_path):
    file_list = os.listdir(input_folder)
    df = pd.read_csv(csv_path, dtype=str)

    for file in file_list:
        if file.endswith(".pdf") and file not in ["170.pdf", "171.pdf", "354.pdf"]:
            print(f"Processing {file}")
            file_name = os.path.splitext(file)[0]
            row = df[df['fileName'] == file_name]

            if not row.empty:
                should_value = row['comments'].values[0]
                first_line = should_value.split("\n")[0]

                update_comments_in_pdf(os.path.join(input_folder, file), first_line, output_path)
                print(f"{file} updated with comment {first_line}")

output_path = r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments"
input_folder = r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2"
csv_path = r"C:\python\scripts\pdfeditor2\processing\combined_output.csv"

loop_folder_comments(input_folder, csv_path, output_path)
