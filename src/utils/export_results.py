import openpyxl

def export_results_to_excel(results_array, output_file="results.xlsx"):
    """
    ~~Append each item from results_array as a row in output_file
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Results"

    if not results_array:
        print("⚠️ No results to export.")
        return
    
    headers = list(results_array[0].keys())
    ws.append(headers)

    for item in results_array:
        row = [item.get(header, "") for header in headers]
        ws.append(row)

    wb.save(output_file)
    print(f"✅ Results exported to {output_file}")
