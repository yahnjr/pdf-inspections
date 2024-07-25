import pdfrw


def print_form_fields(pdf_path):
    # Read the PDF file
    pdf_document = pdfrw.PdfReader(pdf_path)

    # Get the AcroForm fields
    annotations = pdf_document.pages[0]["/Annots"]

    if annotations:
        for annotation in annotations:
            field = annotation["/T"]
            field_value = annotation["/V"]
            print(f"{field}")


# Path to your PDF file
pdf_path = r"C:\Users\ianm\Downloads\perpendicular.pdf"

# Print the form fields
print_form_fields(pdf_path)

import pandas as pd
from pdfrw import PdfReader, PdfWriter, PdfDict


def fill_pdf_form(pdf_template_path, data, lookup, output_path):
    # Read the PDF template
    template_pdf = PdfReader(pdf_template_path)
    # Track if any fields were updated
    fields_updated = False

    for page_number, page in enumerate(template_pdf.pages, start=1):
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation.get("/Subtype") == "/Widget":
                    field = annotation.get("/T")
                    if field:
                        field_name = str(field).strip("()")  # Remove parentheses
                        if field_name in lookup:
                            data_field_name = lookup[field_name]
                            if pd.notna(data_field_name) and data_field_name in data:
                                field_value = str(data[data_field_name])
                                print(
                                    f'Page {page_number}: Updating field "{field_name}" with value "{field_value}"'
                                )
                                annotation.update(
                                    PdfDict(
                                        V=field_value,
                                        AP=None,  # Remove appearance stream
                                    )
                                )
                                fields_updated = True
                            else:
                                print(
                                    f'Page {page_number}: No data for PDF field "{field_name}" (Excel field "{data_field_name}")'
                                )
                        else:
                            print(
                                f'Page {page_number}: PDF field "{field_name}" not found in lookup dictionary'
                            )
                    else:
                        print(f"Page {page_number}: Annotation without a field name")

    if not fields_updated:
        print(
            "No fields were updated. Please check the PDF form fields and the lookup table."
        )

    # Write out the updated PDF
    PdfWriter().write(output_path, template_pdf)


# Read the Excel file
excel_path = r"C:\python\scripts\pdfeditor2\50.xlsx"
data_df = pd.read_excel(excel_path)

# Read the lookup CSV file and handle parentheses and blanks
lookup_path = r"C:\python\scripts\pdfeditor2\perp_lookup.csv"
lookup_df = pd.read_csv(lookup_path)

# Remove rows with blank pdfField values
lookup_df = lookup_df.dropna(subset=["pdfField"])

# Remove parentheses from pdfField values
lookup_df["pdfField"] = lookup_df["pdfField"].str.strip("()")

# Create lookup dictionary
lookup_dict = pd.Series(lookup_df.dataField.values, index=lookup_df.pdfField).to_dict()

# Loop through each row in the Excel file and fill the PDF form
for index, row in data_df.iterrows():
    pdf_template_path = r"C:\python\scripts\pdfeditor2\docs\perpendicular.pdf"
    output_path = f"C:\\python\\scripts\\pdfeditor2\\output_{index}.pdf"
    fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)
