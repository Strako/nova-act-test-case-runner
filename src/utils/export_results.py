import openpyxl
from .export_utils import process_results_with_raw_program_body, _format_cell_value, _create_excel_row

def export_results_to_excel(results_array, output_file="results.xlsx"):
    """
    Export each item from results_array as a row in output_file with rawProgramBody data
    """
    # Process results to include rawProgramBody data
    processed_results = process_results_with_raw_program_body(results_array)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Results"

    if not processed_results:
        print("⚠️ No results to export.")
        return
    
    headers = list(processed_results[0].keys())
    ws.append(headers)

    for item in processed_results:
        row = _create_excel_row(item, headers)
        ws.append(row)

    wb.save(output_file)
    print(f"✅ Results exported to {output_file}")
