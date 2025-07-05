from django.conf import settings
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

def generate_excel_from_schema(schema, filename="output.xlsx", row_limit=100):
    file_name="user_data_template.xlsx"
    downloads_folder = settings.MEDIA_ROOT / 'downloads'
    downloads_url = '/media/downloads'
    file_path = f'{downloads_folder}/{file_name}'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data Entry"

    # Write headers
    headers = [col["name"] for col in schema]
    ws.append(headers)

    for idx, col in enumerate(schema):
        col_letter = get_column_letter(idx + 1)
        validation_range = f"{col_letter}2:{col_letter}{row_limit}"

        # Prepare validation kwargs dynamically
        v_args = col.get("validation", {})
        if not v_args:
            continue  # Skip if no validation
        
        # Create validation object
        dv = DataValidation(**v_args)

        # Add validation to worksheet and to the correct range
        ws.add_data_validation(dv)
        dv.add(validation_range)

        # Optional: if type is 'date', format the cells as date
        if v_args.get("type") == "date":
            for row in range(2, row_limit + 1):
                ws[f"{col_letter}{row}"].number_format = "yyyy-mm-dd"

    # Save workbook
    wb.save(file_path)
    print(f"Excel file saved as '{filename}'")
    return f'{downloads_url}/{file_name}'

