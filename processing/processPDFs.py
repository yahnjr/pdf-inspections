from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfString
import pandas as pd
import os

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
                                    if field_name.endswith("_PASS"):
                                        if (
                                            field_value.lower() == "pass"
                                            or field_value.lower() == "y"
                                        ):
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"  Checkbox selected: {field_name}")
                                        else:
                                            # Automatically find and fill the corresponding _FAIL field
                                            fail_field_name = field_name.replace(
                                                "_PASS", "_FAIL"
                                            )
                                            print(
                                                f"  Looking for corresponding fail field: {fail_field_name}"
                                            )
                                            for fail_annotation in annotations:
                                                fail_field = fail_annotation.get("/T")
                                                if (
                                                    fail_field
                                                    and fail_field_name
                                                    in str(fail_field)
                                                ):
                                                    fail_annotation.update(
                                                        PdfDict(
                                                            AS=PdfName("Yes"),
                                                            V=PdfName("Yes"),
                                                        )
                                                    )
                                                    fields_updated = True
                                                    print(
                                                        f"  Checkbox selected for fail: {fail_field_name}"
                                                    )
                                                    break
                                            else:
                                                print(
                                                    f"  Corresponding fail field not found for: {fail_field_name}"
                                                )

                                    elif field_name.endswith("TRVRSBLE"):
                                        if field_value == "Y":
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"   Checkbox selected: {field_name}")
                                    elif field_name.endswith("_PRSNT"):
                                        if field_value.lower() == "none":
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"   Checkbox selected: {field_name}")
                                        elif field_value.lower() == "turn-space":
                                            turn_space_field = "TURN_SPACE_PRSNT"
                                            for turn_space_annotation in annotations:
                                                turn_space = turn_space_annotation.get(
                                                    "/T"
                                                )
                                                if (
                                                    turn_space
                                                    and turn_space_field
                                                    == str(turn_space)
                                                ):
                                                    turn_space_annotation.update(
                                                        PdfDict(
                                                            AS=PdfName("Yes"),
                                                            V=PdfName("Yes"),
                                                        )
                                                    )
                                                    fields_updated = True
                                                    print(
                                                        f"Turn space selected for {turn_space_field}"
                                                    )
                                                    break
                                            else:
                                                print(
                                                    f"Failed to find turn space field: {turn_space_field}"
                                                )
                                        elif field_value.lower() == "landing":
                                            landing_field = "LANDING_PRSNT"
                                            for landing_annotation in annotations:
                                                landing = landing_annotation.get("/T")
                                                if landing and landing_field == str(
                                                    landing
                                                ):
                                                    landing_annotation.update(
                                                        PdfDict(
                                                            AS=PdfName("Yes"),
                                                            V=PdfName("Yes"),
                                                        )
                                                    )
                                                    fields_updated = True
                                                    print(
                                                        f"Landing selected for {landing_field}"
                                                    )
                                                    break
                                            else:
                                                print(
                                                    f"Failed to find landing field: {landing_field}"
                                                )

                                        else:
                                            print(
                                                f"Error finding value for {field_name}"
                                            )
                                    else:
                                        print(
                                            f"  Checkbox field doesn't match with existing protocols: {field_name}"
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

output_folder = r"C:\python\scripts\pdfeditor2\processing\output"

# Remove rows with blank pdfField values and create lookup dictionary
lookup_df = lookup_df.dropna(subset=["pdfField"])
lookup_dict = pd.Series(lookup_df.csvField.values, index=lookup_df.pdfField).to_dict()

print(lookup_dict)


# Process each row in the combined CSV file
def process_csv_rows(data_df, output_folder):
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
        output_path = os.path.join(output_folder, output_file_name)

        # Fill the PDF form with the current row data
        print(f"Now processing {file_name}")
        fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)


process_csv_rows(data_df, output_folder)
print(f"All rows in {combined_csv_path} processed and saved in {output_folder}")


def process_specific_row(data_df, output_folder, row_index):
    try:
        # Get the specific row by index
        row = data_df.iloc[row_index]
    except IndexError:
        print(f"Error: Row index {row_index} is out of bounds.")
        return

    ramp_type = row["type"]
    file_name = row["fileName"]

    # Handle potential NaN values in fileName
    if pd.isna(file_name):
        print(f"Skipping row {row_index} due to missing fileName")
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
    output_path = os.path.join(output_folder, output_file_name)

    # Fill the PDF form with the current row data
    print(f"Now processing row {row_index} with fileName '{file_name}'")
    fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)


process_specific_row(data_df, output_folder, 180)
