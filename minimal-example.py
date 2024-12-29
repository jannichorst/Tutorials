from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral

pdf_path = 'path/to/sample.pdf'
pages_data = {}

with open(pdf_path, 'rb') as file:
    # Step 1: Parse the PDF document.
    parser = PDFParser(file)
    doc = PDFDocument(parser)

    # Step 2: Extract form fields from the AcroForm section of the document catalog.
    fields = resolve1(doc.catalog['AcroForm']).get('Fields', [])
    field_id = 1  # A unique identifier for fields

    # Step 3: Iterate through pages.
    for page_num, page in enumerate(PDFPage.create_pages(doc)):
        page_number = page_num + 1
        # Initialize a dictionary to store field data for this page
        pages_data[page_number] = {'fields': []}

        # Step 4: Process annotations on the page.
        if page.annots:
            # Step 5: Resolve annotation references.
            annots = resolve1(page.annots)
            for annot in annots:
                # Step 6: Check if the annotation is of type 'Widget'.
                annot_obj = resolve1(annot)
                if annot_obj.get('Subtype') == PSLiteral('Widget'):
                    # Step 7: Determine the field object.
                    parent = annot_obj.get('Parent')
                    field_obj = resolve1(parent) if parent else annot_obj

                    # Step 8: Extract the field name ('T') and field value ('V').
                    field_name = field_obj.get('T')
                    field_value = resolve1(field_obj.get('V')) if field_obj.get('V') else None

                    # Step 9: Decode and store extracted details.
                    pages_data[page_number]['fields'].append({
                        'field_id': field_id,  # Unique identifier for the field
                        'name': field_name.decode('utf-8') if field_name else None,  # Decode 'T' as a string
                        'value': field_value.decode('utf-8') if field_value else None,  # Decode 'V' as a string
                    })
                    field_id += 1
