import os
import json
import glob
from typing import List, Dict, Any

logs_directory = os.getenv("LOGS_DIRECTORY")

def _extract_raw_program_body_from_item(item: Dict[str, Any]) -> str | None:
    """Extract rawProgramBody from a single JSON item."""
    if not isinstance(item, dict) or 'response' not in item:
        return None
    
    response = item['response']
    if not isinstance(response, dict) or 'rawProgramBody' not in response:
        return None
    
    raw_program_body = response['rawProgramBody']
    return raw_program_body if isinstance(raw_program_body, str) else None


def _process_json_file(json_file: str) -> List[str]:
    """Process a single JSON file and extract all rawProgramBody strings."""
    raw_program_bodies = []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        if not isinstance(json_data, list):
            return raw_program_bodies
        
        for item in json_data:
            raw_program_body = _extract_raw_program_body_from_item(item)
            if raw_program_body:
                raw_program_bodies.append(raw_program_body)
    
    except (json.JSONDecodeError, IOError, KeyError) as e:
        print(f"Warning: Could not process file {json_file}: {e}")
    
    return raw_program_bodies


def _get_raw_program_bodies_for_session(session_id: str) -> List[str]:
    """Get all rawProgramBody strings for a given session_id."""
    temp_folder_pattern = f"{logs_directory}{session_id}"
    raw_program_bodies = []
    
    if not (os.path.exists(temp_folder_pattern) and os.path.isdir(temp_folder_pattern)):
        return raw_program_bodies
    
    json_files = glob.glob(os.path.join(temp_folder_pattern, "*.json"))
    
    for json_file in json_files:
        file_raw_program_bodies = _process_json_file(json_file)
        raw_program_bodies.extend(file_raw_program_bodies)
    
    return raw_program_bodies


def _process_single_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single result object to add rawProgramBody data."""
    processed_result = result.copy()
    session_id = result.get('session_id')
    
    if not session_id:
        processed_result['rawProgramBody'] = []
        return processed_result
    
    raw_program_bodies = _get_raw_program_bodies_for_session(session_id)
    processed_result['rawProgramBody'] = raw_program_bodies
    
    return processed_result


def process_results_with_raw_program_body(results_array: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process results_array by adding rawProgramBody data from corresponding JSON files.
    
    Args:
        results_array: List of result objects containing session_id attribute
        
    Returns:
        List of result objects with added rawProgramBody data
    """
    return [_process_single_result(result) for result in results_array]


def _format_cell_value(header: str, value: Any) -> str:
    """Format a cell value for Excel export."""
    if header == 'rawProgramBody' and isinstance(value, list):
        return '\n'.join(value)
    return value if value is not None else ""


def _create_excel_row(result: Dict[str, Any], headers: List[str]) -> List[str]:
    """Create a row for Excel export from a result object."""
    return [_format_cell_value(header, result.get(header, "")) for header in headers]


