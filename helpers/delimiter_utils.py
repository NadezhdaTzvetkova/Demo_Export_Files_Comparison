import pandas as pd
import re
import logging
from collections import Counter
from typing import List, Optional


# =================== Extended DELIMITER_MAPPING ===================
# Map human-readable delimiter names to actual characters.
DELIMITER_MAPPING = {
    "comma": ",",  # Comma (CSV, common)
    "semicolon": ";",  # Semicolon (Used in European CSV files)
    "TAB": "\t",  # Tab (TSV, Excel sheets)
    "pipe": "|",  # Pipe (Used in pipe-separated files)
    "space": " ",  # Space (Used in some non-standard files)
    "colon": ":",  # Colon (rare but sometimes used)
    "tilde": "~",  # Tilde (used occasionally)
    "caret": "^",  # Caret (uncommon, used for special cases)
    "quote": "\"",  # Quote (used to enclose fields in CSV/Excel)
}

# =================== Valid and Invalid Delimiters for File Types ===================
VALID_DELIMITERS = {
    "csv": [
        "comma",
        "semicolon",
        "TAB",
        "pipe",
    ],  # CSV files: comma, semicolon, tab, pipe
    "tsv": ["TAB", "comma", "pipe"],  # TSV files: tab, pipe (comma is optional)
    "excel": [
        "comma",
        "semicolon",
        "TAB",
        "pipe",
    ],  # Excel sheets: comma, semicolon, tab, pipe
}

INVALID_DELIMITERS = {
    "csv": ["space", "colon", "tilde", "caret", "quote"],  # Invalid for CSV files
    "tsv": ["comma", "semicolon", "space", "quote"],  # Invalid for TSV files
    "excel": ["space", "tilde", "caret"],  # Invalid for Excel files
}

# =================== Functions for Delimiter Detection ===================


def get_valid_delimiters(file_type: str) -> List[str]:
    """Returns the valid delimiters for a given file type."""
    return [DELIMITER_MAPPING[d] for d in VALID_DELIMITERS.get(file_type, [])]


def get_invalid_delimiters(file_type: str) -> List[str]:
    """Returns the invalid delimiters for a given file type."""
    return [DELIMITER_MAPPING[d] for d in INVALID_DELIMITERS.get(file_type, [])]


def escape_delimiter_in_file(file_path: str, delimiter: str) -> str:
    """Escape the delimiter inside quoted fields in a file to avoid false positives."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Escape delimiters inside quotes to avoid confusion with the actual delimiter
    content = re.sub(
        r'(".*?")', lambda m: m.group(0).replace(delimiter, f"\\{delimiter}"), content
    )
    return content


def detect_delimiters_in_csv(file_path: str, check_all_lines: bool = True) -> List[str]:
    """Detects possible delimiters in a CSV file based on the content."""
    detected_delimiters: List[str] = []  # List to store detected delimiters
    delimiter_counts: Counter[str] = (
        Counter()
    )  # Counter to count occurrences of each delimiter

    # Read file and check delimiters
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Escape delimiters inside quotes to avoid false matches
    for delimiter_name, delimiter in DELIMITER_MAPPING.items():
        escaped_content = escape_delimiter_in_file(file_path, delimiter)

        # Check all lines or just the first line
        lines_to_check = lines if check_all_lines else [lines[0]]

        for line in lines_to_check:
            if delimiter in line:
                delimiter_counts[delimiter] += 1

    detected_delimiters = list(delimiter_counts.keys())

    # Handle cases where multiple delimiters are found
    if len(detected_delimiters) > 1:
        logging.warning(
            f"Multiple delimiters detected: {detected_delimiters}. This might indicate an inconsistency."
        )

    return detected_delimiters


def detect_delimiters_in_excel(
    file_path: str, sheet_name: Optional[str] = None, check_all_rows: bool = True
) -> List[str]:
    """Detects possible delimiters in an Excel sheet by checking the first row or all rows."""
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    first_line = df.iloc[0].astype(str).str.cat(sep=',')

    detected_delimiters: List[str] = []

    # Escape delimiters inside quotes to avoid false matches
    for delimiter_name, delimiter in DELIMITER_MAPPING.items():
        if delimiter in first_line:
            detected_delimiters.append(delimiter)

    if check_all_rows:
        # Check other rows for consistency (optional)
        for _, row in df.iterrows():
            row_str = row.astype(str).str.cat(sep=',')
            for delimiter_name, delimiter in DELIMITER_MAPPING.items():
                if delimiter in row_str:
                    detected_delimiters.append(delimiter)

    return detected_delimiters


# =================== Delimiter Validation ===================


def validate_allowed_delimiters(allowed_delimiters: str, file_type: str) -> List[str]:
    """Validates and returns the list of delimiters based on user input."""
    allowed_list = [DELIMITER_MAPPING[d.strip()] for d in allowed_delimiters.split(",")]

    valid_delimiters = get_valid_delimiters(file_type)
    invalid_delimiters = get_invalid_delimiters(file_type)

    # Check if allowed delimiters are valid for the file type
    for d in allowed_list:
        if d not in valid_delimiters:
            raise ValueError(f"Delimiter '{d}' is not valid for {file_type} files.")
        if d in invalid_delimiters:
            raise ValueError(
                f"Delimiter '{d}' is considered invalid for {file_type} files."
            )

    return allowed_list


# =================== Helper to Detect File Type and Return Delimiters ===================


def detect_delimiters(
    file_path: str, file_type: str, sheet_name: Optional[str] = None
) -> List[str]:
    """Detects delimiters based on file type and returns the valid delimiters."""
    if file_type == "csv":
        return detect_delimiters_in_csv(file_path)
    elif file_type == "excel":
        return detect_delimiters_in_excel(file_path, sheet_name)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


# =================== File Integrity Validation ===================


def validate_file_integrity(
    file_path: str, expected_delimiters: List[str], file_type: str
) -> bool:
    """Validates that the file conforms to the expected delimiter structure."""
    detected_delimiters = detect_delimiters(file_path, file_type)

    if set(detected_delimiters) != set(expected_delimiters):
        logging.error(
            f"Detected delimiters {detected_delimiters} do not match expected {expected_delimiters}"
        )
        return False

    return True


def check_for_inconsistent_delimiters(file_path: str) -> List[str]:
    """Check for inconsistent delimiters within a file."""
    delimiter_counts: Counter[str] = Counter()  # Type annotation added

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for delimiter_name, delimiter in DELIMITER_MAPPING.items():
                if delimiter in line:
                    delimiter_counts[delimiter] += 1

    most_common_delimiter = delimiter_counts.most_common(1)

    if len(delimiter_counts) > 1:
        logging.warning(
            "Inconsistent delimiters detected: {}. Majority delimiter: {}".format(
                delimiter_counts, most_common_delimiter[0]
            )
        )

    return list(delimiter_counts.keys())


def check_for_tab_or_pipe(file_path: str) -> bool:
    """Check if the file contains TAB or pipe delimiters."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "\t" in line or "|" in line:
                logging.info("TAB or pipe delimiter detected.")
                return True
    return False


def handle_escaped_delimiters(file_path: str, delimiter: str) -> bool:
    """Check and handle delimiters inside quotes for CSV/Excel."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    escaped_delimiters = re.findall(r'(".*?")', content)
    for group in escaped_delimiters:
        if delimiter in group:
            logging.warning(
                f"Delimiter {delimiter} found inside quotes, which might lead to incorrect parsing."
            )
            return True

    return False


def validate_delimiters_for_excel(
    file_path: str, sheet_name: Optional[str] = None
) -> List[str]:
    """Validate delimiters for an Excel file."""
    return detect_delimiters_in_excel(file_path, sheet_name, check_all_rows=True)
