from PyPDF2 import PdfReader, PdfWriter

def change_field_to_text(input_pdf, output_pdf, field_name):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Copy all pages from the input PDF to the output PDF
    for page in reader.pages:
        writer.add_page(page)

    # Get the form fields
    writer.update_page_form_field_values(
        writer.pages[0], reader.get_form_text_fields()
    )

    # Modify the specified field to be a text input
    for field in reader.get_fields():
        if field == field_name:
            writer.update_page_form_field_values(
                writer.pages[0],
                {field_name: ""}
            )
            field_obj = reader.get_fields()[field]
            field_obj.update({
                "/FT": "/Tx",  # Change field type to text
                "/Ff": 0  # Remove any flags (like readonly)
            })

    # Write the modified PDF to the output file
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

# Usage
input_pdf = r"C:\python\scripts\pdfeditor2\docs\combination.pdf"
output_pdf = r"C:\python\scripts\pdfeditor2\docs\combination2.pdf"
field_name = "ADA2_SIGNAL_TYPE"

change_field_to_text(input_pdf, output_pdf, field_name)

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fill_choice_field(input_pdf, output_pdf, field_name, choice_value):
    try:
        # Load the PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        logger.info(f"Opened PDF: {input_pdf}")

        # Assuming the form is on the first page
        page = reader.pages[0]
        writer.add_page(page)

        # Get all form fields
        fields = reader.get_fields()

        if field_name not in fields:
            logger.error(f"Field '{field_name}' not found in the PDF")
            return

        field = fields[field_name]
        if field.get('/FT') == '/Ch':  # Check if it's a choice field
            options = field.get('/Opt')
            logger.info(f"Possible values for {field_name}: {options}")

            # Try to find the index of the choice_value
            try:
                choice_index = options.index(choice_value)
                logger.info(f"Found '{choice_value}' at index {choice_index}")
            except ValueError:
                logger.warning(f"'{choice_value}' not found in options. Will try direct value.")
                choice_index = None

            # Update the field with the choice index or direct value
            if choice_index is not None:
                field.update({
                    '/V': choice_value,
                    '/Opt': options
                })
            else:
                field.update({
                    '/V': choice_value
                })

            logger.info(f"Updated field '{field_name}' to value: {choice_value}")
        else:
            logger.warning(f"Field '{field_name}' is not a choice field. Attempting to update anyway.")
            field.update({
                '/V': choice_value
            })

        # Write the updated PDF to the output file
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

        logger.info(f"PDF written to {output_pdf}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

# Usage
fill_choice_field(input_pdf, output_pdf, field_name, "SY")

def fill_choice_field_by_index(input_pdf, output_pdf, field_name, choice_index):
    try:
        # Load the PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Assuming the form is on the first page
        page = reader.pages[0]
        writer.add_page(page)

        # Get all form fields
        fields = reader.get_fields()

        if field_name not in fields:
            print(f"Field '{field_name}' not found in the PDF")
            return

        field = fields[field_name]
        if field.get('/FT') == '/Ch':  # Check if it's a choice field
            options = field.get('/Opt')

            if choice_index < 0 or choice_index >= len(options):
                print(f"Invalid choice index: {choice_index}")
                return

            # Update the field with the choice index
            field_value = options[choice_index]
            writer.update_page_form_field_values(writer.pages[0], {field_name: field_value})

            # Ensure the field is set to the new value
            field['/V'] = field_value
            field['/AS'] = field_value

            print(f"Successfully updated field '{field_name}' with value '{field_value}'")
        else:
            print(f"Field '{field_name}' is not a choice field")
            return

        # Write the updated PDF to the output file
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

fill_choice_field_by_index(input_pdf, output_pdf, field_name, 1)