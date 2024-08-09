###Read form fields from pdfs###
import PyPDF2


def list_pdf_fields(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as pdf_file:
        # Initialize the PdfFileReader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Check if the PDF has form fields
        if len(pdf_reader.pages) > 0 and "/AcroForm" in pdf_reader.trailer["/Root"]:
            form = pdf_reader.trailer["/Root"]["/AcroForm"]
            fields = form["/Fields"]

            # Iterate through the form fields
            for field in fields:
                field_obj = field.get_object()
                field_name = field_obj.get("/T")
                field_type = field_obj.get("/FT")
                field_value = field_obj.get("/V", "")

                # Determine the field type
                if field_type == "/Tx":
                    field_type = "Text"
                elif field_type == "/Btn":
                    field_type = "Button"
                elif field_type == "/Ch":
                    field_type = "Choice"
                elif field_type == "/Sig":
                    field_type = "Signature"
                else:
                    field_type = "Unknown"

                print(
                    f"Field Name: {field_name}, Field Type: {field_type}, Field value: {field_value}"
                )
        else:
            print("No form fields found in this PDF.")


# Path to your PDF file
pdf_path = r"C:\python\scripts\pdfeditor2\docs\perpendicular.pdf"

# List the PDF fields
list_pdf_fields(pdf_path)

###Download attachments and concatenate them into one table (requires manual cleanup)

from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import os
import pandas as pd
import getpass
import shutil

username = input("Enter your ArcGIS Online username: ")

password = getpass.getpass("Enter your ArcGIS Online password: ")

# Authenticate with ArcGIS Online
gis = GIS("https://3j.maps.arcgis.com", username, password)

# Access the feature layer
feature_layer_url = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6_results/FeatureServer/0"
layer = FeatureLayer(feature_layer_url)

# Specify the folder to save attachments
output_folder = r"C:\python\scripts\pdfeditor2\processing\downloads"
os.makedirs(output_folder, exist_ok=True)

# Query the layer to get all features
features = layer.query().features

if features:
    print(features[0].attributes)

# Initialize a list to store DataFrames
object_id_field = "objectid"

# Specify the file types to download
allowed_extensions = [".xlsx", ".xls"]

# Print features with their attachments
if features:
    for feature in features:
        feature_id = feature.attributes[object_id_field]
        attachments = layer.attachments.get_list(feature_id)
        if attachments:
            print(f"Feature {feature_id} has the following attachments:")
            for attachment in attachments:
                attachment_name = attachment["name"]
                attachment_extension = os.path.splitext(attachment_name)[1].lower()
                if attachment_extension in allowed_extensions:
                    print(f"  - {attachment_name} (ID: {attachment['id']})")
else:
    print("No features found in the layer.")

allowed_extensions = [".jpg", ".jpeg"]

# Attempting re-run with images
if features:
    for feature in features:
        feature_id = feature.attributes[object_id_field]
        attachments = layer.attachments.get_list(feature_id)
        if attachments:
            print(f"Feature {feature_id} has the following attachments:")
            for attachment in attachments:
                attachment_name = attachment["name"]
                attachment_extension = os.path.splitext(attachment_name)[1].lower()
                if attachment_extension in allowed_extensions:
                    print(f"  - {attachment_name} (ID: {attachment['id']})")
else:
    print("No features found in the layer.")

# Download the allowed attachments
if features:
    for feature in features:
        try:
            feature_id = feature.attributes[object_id_field]
            attachments = layer.attachments.get_list(feature_id)

            if feature_id > 124:
                for attachment in attachments:
                    attachment_name = attachment["name"]
                    attachment_extension = os.path.splitext(attachment_name)[1].lower()

                    if attachment_extension in allowed_extensions:
                        attachment_id = attachment["id"]
                        final_output = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\{feature_id}-{attachment_id}{attachment_extension}"
                        temp_output = f"C:\\python\\scripts\\pdfeditor2\\processing\\downloads\\attachments\\temp"

                        # Debug: Print before download
                        print(
                            f"Attempting to download attachment {attachment_id} for feature {feature_id}"
                        )

                        # Download attachment
                        attachment_url = layer.attachments.download(
                            feature_id, attachment_id, save_path=temp_output
                        )

                        # Debug: Check if download succeeded
                        if os.path.exists(temp_output):
                            print(
                                f"Downloaded attachment {attachment_id} to {temp_output}"
                            )
                            os.rename(
                                os.path.join(temp_output, attachment_name),
                                f"{feature_id}-{attachment_id}{attachment_extension}",
                            )
                            print(
                                f"Saved as {feature_id}-{attachment_id}{attachment_extension}"
                            )
                        else:
                            print(
                                f"Failed to download or locate the file at {temp_output}"
                            )

        except Exception as e:
            print(f"Error processing feature {feature_id}: {e}")
else:
    print("No features found in the layer.")

print("All specified attachments have been downloaded.")
print("All attachments have been downloaded.")

dataframes = []

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
combined_output_path = r"C:\python\scripts\pdfeditor2\processing\combined_output1.xlsx"
combined_df.to_excel(combined_output_path, index=False)

print(f"All tables have been combined and saved to {combined_output_path}")

print(combined_df.head())

field_names_df = [name.replace("-", "_") for name in combined_df.columns.tolist()]

print(field_names_df)

df = pd.read_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output1.csv")
remove_vowels = lambda text: "".join(
    char for char in text if char.lower() not in "aeiou"
)

field_names = [
    remove_vowels(name) if len(name) > 13 else name for name in field_names_df
]


def remove_vowels(text):
    return "".join(char for char in text if char.lower() not in "aeiou")


# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output1.csv")

# Get the original field names
original_field_names = list(df.columns)

# Modify field names based on the provided logic
field_names = [
    remove_vowels(name) if len(name) > 13 else name for name in original_field_names
]

# Assign the new field names to the DataFrame
df.columns = field_names

# Optionally, write the modified DataFrame to a new CSV file
df.to_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output1.csv", index=False)
###Fill out Pdfs


import PyPDF2
import pandas as pd


def fill_pdf(pdf_path, output_path, data, field_mapping):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        if pdf_reader.getNumPages() > 0 and "/AcroForm" in pdf_reader.trailer["/Root"]:
            print(f"PDF has {pdf_reader.getNumPages()} pages and contains form fields.")
            form = pdf_reader.trailer["/Root"]["/AcroForm"]
            fields = form["/Fields"]

            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

            for field in fields:
                field_obj = field.getObject()
                pdf_field_name = field_obj.get("/T")

                if pdf_field_name:
                    pdf_field_name = pdf_field_name.strip()
                    print(f"Found field in PDF: {pdf_field_name}")

                if pdf_field_name in field_mapping:
                    csv_field_name = field_mapping[pdf_field_name]
                    if csv_field_name in data:
                        field_value = data[csv_field_name]
                        print(
                            f"Filling field '{pdf_field_name}' with value '{field_value}' from CSV field '{csv_field_name}'"
                        )
                        field_obj.update(
                            {
                                PyPDF2.generic.NameObject(
                                    "/V"
                                ): PyPDF2.generic.createStringObject(str(field_value)),
                                PyPDF2.generic.NameObject(
                                    "/Ff"
                                ): PyPDF2.generic.NumberObject(1),
                            }
                        )
                    else:
                        print(f"CSV field '{csv_field_name}' not found in data.")
                else:
                    print(f"PDF field '{pdf_field_name}' not found in field mapping.")

            pdf_writer.addJS("this.flattenPages();")
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)
            print(f"PDF saved to {output_path}")
        else:
            print("No form fields found in this PDF or PDF is empty.")


def process_csv(csv_path, lookup_path, output_folder):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    print(f"CSV data read from {csv_path}:\n{df.head()}")

    # Read the lookup table
    lookup_df = pd.read_csv(lookup_path)
    print(f"Lookup table read from {lookup_path}:\n{lookup_df.head()}")
    field_mapping = dict(
        zip(lookup_df["lookup"].str.strip(), lookup_df["field"].str.strip())
    )
    print(f"Field mapping: {field_mapping}")

    # Process the first row
    if not df.empty:
        first_row = df.iloc[10]
        print(f"Processing first row of CSV: {first_row}")
        file_type = first_row["type"]
        file_name = first_row["fileName"]

        pdf_path = f"C:\\python\\scripts\\pdfeditor2\\docs\\{file_type}.pdf"
        output_path = f"{output_folder}\\{file_name}.pdf"

        data = first_row.to_dict()
        fill_pdf(pdf_path, output_path, data, field_mapping)
    else:
        print("CSV file is empty.")


# Paths to the CSV files and the output folder
csv_path = r"C:\python\scripts\pdfeditor2\processing\combined_output.csv"
lookup_path = r"C:\python\scripts\pdfeditor2\processing\lookup.csv"
output_folder = r"C:\python\scripts\pdfeditor2\processing\output"

# Process the CSV and fill the PDF
process_csv(csv_path, lookup_path, output_folder)


###Previous pdf fill-out functions

from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfString
import pandas as pd


def format_choice_value(value):
    """Format the value for comparison with list box options."""
    return str(value).strip().lower()


def combobox(annotation, value):
    export = None
    formatted_value = format_choice_value(value)
    for each in annotation["/Opt"]:
        if isinstance(each, list) and len(each) > 1:
            if format_choice_value(each[1].to_unicode()) == formatted_value:
                export = each[0].to_unicode()
        elif isinstance(each, PdfString):
            if format_choice_value(each.to_unicode()) == formatted_value:
                export = each.to_unicode()
    if export is None:
        print(f"Warning: Export Value for '{value}' Not Found. Using the value as is.")
        export = value
    pdfstr = PdfString.encode(export)
    annotation.update(PdfDict(V=pdfstr, AS=pdfstr))


def fill_pdf_form(pdf_template_path, data, lookup, output_path):
    template_pdf = PdfReader(pdf_template_path)
    fields_updated = False

    print("\nProcessing PDF fields:")
    for page in template_pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation.get("/Subtype") == "/Widget":
                    field = annotation.get("/T")
                    if field:
                        field_name = (
                            field[1:-1]
                            if field.startswith("(") and field.endswith(")")
                            else field
                        )
                        field_type = annotation.get("/FT")
                        print(f"\nField: {field_name}")
                        print(f"  Type: {field_type}")

                        if field_name in lookup:
                            data_field_name = lookup[field_name]
                            print(f"  Mapped to CSV column: {data_field_name}")
                            if data_field_name in data and pd.notna(
                                data[data_field_name]
                            ):
                                field_value = str(data[data_field_name])

                                if field_type == PdfName("Tx"):  # Text field
                                    annotation.update(
                                        PdfDict(V=field_value, AP=PdfDict())
                                    )
                                    fields_updated = True
                                    print(f"  Text value filled: {field_value}")

                                elif field_type == PdfName(
                                    "Ch"
                                ):  # Choice field (combobox/dropdown)
                                    try:
                                        combobox(annotation, field_value)
                                        fields_updated = True
                                        print(
                                            f"  Combobox value selected: {field_value}"
                                        )
                                    except Exception as e:
                                        print(
                                            f"  Error setting combobox value: {str(e)}"
                                        )

                                elif field_type == PdfName("Btn"):  # Checkbox
                                    if field_name.endswith(
                                        "_PASS"
                                    ) or field_name.endswith("_FAIL"):
                                        if (
                                            field_name.endswith("_PASS")
                                            and field_value.lower() == "pass"
                                        ) or (
                                            field_name.endswith("_FAIL")
                                            and field_value.lower() == "fail"
                                        ):
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"  Checkbox selected: {field_name}")
                                        else:
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Off"), V=PdfName("Off")
                                                )
                                            )
                                            print(
                                                f"  Checkbox deselected: {field_name}"
                                            )
                                    else:
                                        print(
                                            f"  Checkbox field doesn't end with _PASS or _FAIL: {field_name}"
                                        )

                                else:
                                    print(f"  Unsupported field type: {field_type}")
                            else:
                                print(f"  No data found in CSV for this field")
                        else:
                            print(f"  Not found in lookup table")

    if not fields_updated:
        print(
            "\nNo fields were updated. Please check the PDF form fields and the lookup table."
        )

    PdfWriter().write(output_path, template_pdf)


# Read the combined CSV file
combined_csv_path = r"C:\python\scripts\pdfeditor2\processing\combined_output.csv"
data_df = pd.read_csv(combined_csv_path)

# Read the lookup CSV file
lookup_path = r"C:\python\scripts\pdfeditor2\processing\lookup.csv"
lookup_df = pd.read_csv(lookup_path)

# Remove rows with blank pdfField values and create lookup dictionary
lookup_df = lookup_df.dropna(subset=["pdfField"])
lookup_dict = pd.Series(lookup_df.csvField.values, index=lookup_df.pdfField).to_dict()


# Process each row in the combined CSV file
for index, row in data_df.iterrows():
    ramp_type = row["type"]
    file_name = row["fileName"]

    # Handle potential NaN values in fileName
    if pd.isna(file_name):
        print(f"Skipping row {index} due to missing fileName")
        continue

    # Use a default name if fileName is not a valid integer
    try:
        output_file_name = f"{int(file_name)}.pdf"
    except ValueError:
        print(
            f"Warning: Invalid fileName '{file_name}' in row {index}. Using index as filename."
        )
        output_file_name = f"output_{index}.pdf"

    pdf_template_path = f"C:\\python\\scripts\\pdfeditor2\\docs\\{ramp_type}.pdf"
    output_path = (
        f"C:\\python\\scripts\\pdfeditor2\\processing\\output\\{output_file_name}"
    )

    # Fill the PDF form with the current row data
    fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)


def process_single_row(data_df, lookup_dict, row_index):
    if row_index < 0 or row_index >= len(data_df):
        print(f"Error: Row index {row_index} is out of bounds.")
        return

    row = data_df.iloc[row_index]
    print(f"\nProcessing row {row_index}:")
    print(row)

    ramp_type = row["type"]
    file_name = row["fileName"]

    # Handle potential NaN values in fileName
    if pd.isna(file_name):
        print(f"Error: Missing fileName for row {row_index}")
        return

    # Use a default name if fileName is not a valid integer
    try:
        output_file_name = f"{int(file_name)}.pdf"
    except ValueError:
        print(
            f"Warning: Invalid fileName '{file_name}' in row {row_index}. Using index as filename."
        )
        output_file_name = f"output_{row_index}.pdf"

    pdf_template_path = f"C:\\python\\scripts\\pdfeditor2\\docs\\{ramp_type}.pdf"
    output_path = (
        f"C:\\python\\scripts\\pdfeditor2\\processing\\output\\{output_file_name}"
    )

    # Fill the PDF form with the current row data
    fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)

    print("\nProcessing complete.")


# Main script
if __name__ == "__main__":
    # Read the combined CSV file
    combined_csv_path = r"C:\python\scripts\pdfeditor2\processing\combined_output.csv"
    data_df = pd.read_csv(combined_csv_path)

    # Read the lookup CSV file
    lookup_path = r"C:\python\scripts\pdfeditor2\processing\lookup.csv"
    lookup_df = pd.read_csv(lookup_path)

    # Remove rows with blank pdfField values and create lookup dictionary
    lookup_df = lookup_df.dropna(subset=["pdfField"])
    lookup_dict = pd.Series(
        lookup_df.csvField.values, index=lookup_df.pdfField
    ).to_dict()

    # Specify which row you want to process (e.g., row index 5)
    row_to_process = 41

    # Process the specified row
    process_single_row(data_df, lookup_dict, row_to_process)
