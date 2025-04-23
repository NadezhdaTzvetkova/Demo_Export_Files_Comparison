import re
import six
import hashlib
import datetime
import logging
import pandas as pd
from typing import List, Any, Optional
from file_processing import *  # Importing memory handling from file_processing.py

# =================== Global variable ===================
historical_records = {}  # type: dict

# =================== Luhn Algorithm ===================


def luhn_check(account_number: str) -> bool:
    """
    Implements the Luhn algorithm for validating account numbers.
    """

    def digits_of(n: str) -> List[int]:
        return [int(d) for d in str(n)]

    digits = digits_of(account_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = sum(odd_digits)  # Sum of odd digits

    for even_digit in even_digits:
        checksum += sum(digits_of(str(even_digit * 2)))  # Convert to string first

    return checksum % 10 == 0


# =================== Column Validation ===================


def is_valid_account_number(account_number: str, pattern: str = r"^\d{10,12}$") -> bool:
    """
    Validates if the provided account number matches the given pattern and Luhn check.

    :param account_number: The account number to validate.
    :param pattern: The regex pattern the account number should match (default checks for 10-12 digits).
    :return: True if the account number matches the pattern and passes Luhn's check, False otherwise.
    """
    # First, check if the account number matches the basic pattern
    if not re.match(pattern, account_number):
        return False

    # If required, apply Luhn's algorithm for further validation
    if not luhn_check(account_number):
        return False

    return True


from typing import Callable


def validate_column(
    df: pd.DataFrame, column_name: str, validation_type: str, **kwargs: Any
) -> bool:
    """Validates individual columns based on their type."""

    # Pre-check if the column exists and is valid
    if column_name not in df.columns:
        logging.warning(
            "Column '{}' does not exist in the DataFrame.".format(column_name)
        )
        return False

    # Define the validation functions
    validation_functions: dict[str, Callable[[], bool]] = {
        "numeric": lambda: pd.api.types.is_numeric_dtype(df[column_name]),
        "unique": lambda: not df[column_name].duplicated().any(),
        "missing": lambda: df[column_name].isnull().any(),
        "date": lambda: pd.to_datetime(df[column_name], errors="coerce").notna().all(),
        "phone": lambda: df[column_name]
        .apply(lambda x: bool(re.match(r"^\+?1?\d{9,15}$", str(x))))
        .all(),
        "email": lambda: df[column_name]
        .apply(
            lambda x: bool(
                re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", str(x))
            )
        )
        .all(),
        "account_number": lambda: df[column_name]
        .apply(lambda x: is_valid_account_number(str(x)))
        .all(),
        "luhn": lambda: df[column_name].apply(lambda x: luhn_check(str(x))).all(),
    }

    # Dynamically evaluate the lambda function for the given validation type
    try:
        # If the validation type exists in the dictionary, apply the lambda function
        if validation_type in validation_functions:
            return validation_functions[validation_type]()  # Call the lambda function

        # Return False if validation type is not recognized
        return False

    except Exception as e:
        logging.error(
            "Error validating column '{}' with type '{}': {}".format(
                column_name, validation_type, str(e)
            )
        )
        return False


# =================== Space Discrepancy Validation ===================


def validate_spaces_in_csv(df, delimiter):
    # type: (pd.DataFrame, str) -> dict
    """
    Identifies and flags space-related discrepancies in the CSV file.
    Checks if there are spaces around the delimiter and logs them.

    :param df: The DataFrame to validate
    :param delimiter: The delimiter used in the CSV file
    :return: A dictionary containing space-related issues or a message if no issues are found
    """
    spaces_found = False
    space_details = {}  # type: dict

    for column in df.columns:
        if df[column].dtype == object:
            df[column] = df[column].str.strip()
            spaces_in_column = df[column].str.contains(
                r"\s*" + re.escape(delimiter) + r"\s*", regex=True
            )
            if spaces_in_column.any():
                spaces_found = True
                space_details[column] = {
                    "total_spaces": spaces_in_column.sum(),
                    "affected_rows": spaces_in_column.sum(),
                    "severity": categorize_severity(spaces_in_column.sum(), len(df)),
                    "rows_with_issues": spaces_in_column.index[
                        spaces_in_column
                    ].tolist(),
                }

    return (
        space_details
        if spaces_found
        else {"No spaces issues detected": "No significant whitespace problems found."}
    )


def categorize_severity(affected_rows: int, total_rows: int) -> str:
    """
    Categorizes the severity of space-related discrepancies based on the percentage
    of affected rows in the column.
    """
    percentage = (affected_rows / total_rows) * 100
    if percentage > 30:
        return "High"
    elif 10 <= percentage <= 30:
        return "Medium"
    else:
        return "Low"


# =================== File Validation ===================


def validate_file(df, column_mappings, file_type="csv"):
    # type: (pd.DataFrame, dict, str) -> dict
    issues = {}  # type: dict

    # 1. Common checks for all file types (CSV/Excel)
    for column in column_mappings.get("numeric_columns", []):
        if not validate_column(df, column, "numeric"):
            issues[column] = "Contains non-numeric values"

    for column in column_mappings.get("unique_columns", []):
        if not validate_column(df, column, "unique"):
            issues[column] = "Contains duplicate values"

    missing_data = sum(
        validate_column(df, column, "missing")
        for column in column_mappings.get("required_columns", [])
    )
    if missing_data > 0:
        issues["missing_data"] = "Missing data in {0} rows".format(missing_data)

    for column, date_format in column_mappings.get("date_columns", {}).items():
        if not validate_column(df, column, "date", date_format=date_format):
            issues[column] = "Invalid date format"

    for column, precision in column_mappings.get("decimal_precision", {}).items():
        if not validate_column(df, column, "numeric"):
            issues[column] = "Invalid decimal precision"

    for column in column_mappings.get("account_number_columns", []):
        if not validate_column(df, column, "account_number"):
            issues[column] = "Invalid account number format"
        if not validate_column(df, column, "luhn"):
            issues[column] = "Invalid account number (Luhn's algorithm)"

    for column in column_mappings.get("email_columns", []):
        if not validate_column(df, column, "email"):
            issues[column] = "Invalid email format"

    for column in column_mappings.get("phone_columns", []):
        if not validate_column(df, column, "phone"):
            issues[column] = "Invalid phone number format"

    # 2. File-type-specific checks for CSV
    if file_type == "csv":
        delimiter = column_mappings.get("delimiter", ",")

        spaces_issues = validate_spaces_in_csv(df, delimiter)
        if spaces_issues:
            issues["spaces"] = spaces_issues

        def validate_csv_delimiters(csv_df, csv_delimiter):
            # type: (pd.DataFrame, str) -> bool
            first_row = (
                csv_df.iloc[0].astype(str).str.contains(re.escape(csv_delimiter))
            )
            return first_row.all()

        if not validate_csv_delimiters(df, delimiter):
            issues["delimiter"] = "Inconsistent delimiters detected in CSV file"

        def validate_csv_headers(csv_df):
            # type: (pd.DataFrame) -> bool
            headers = csv_df.columns
            return all(header.strip() != "" for header in headers)

        if not validate_csv_headers(df):
            issues["headers"] = "Missing or malformed headers in CSV file"

    # 3. File-type-specific checks for Excel
    if file_type == "excel":

        def validate_excel_sheet(excel_sheet_df, excel_column_mappings):
            # type: (pd.DataFrame, dict) -> dict
            sheet_issues_inner = {}  # type: dict

            missing_columns = [
                column
                for column in excel_column_mappings.get("required_columns", [])
                if column not in excel_sheet_df.columns
            ]
            if missing_columns:
                sheet_issues_inner["missing_columns"] = "Missing columns: " + ", ".join(
                    missing_columns
                )

            for column in excel_column_mappings.get("numeric_columns", []):
                if column in excel_sheet_df.columns and not validate_column(
                    excel_sheet_df, column, "numeric"
                ):
                    sheet_issues_inner[column] = "Contains non-numeric values"

            for column in excel_column_mappings.get("unique_columns", []):
                if column in excel_sheet_df.columns and not validate_column(
                    excel_sheet_df, column, "unique"
                ):
                    sheet_issues_inner[column] = "Contains duplicate values"

            return sheet_issues_inner

        if isinstance(df, dict):  # Multi-sheet Excel file
            for sheet_name, sheet_df in df.items():
                sheet_issues = validate_excel_sheet(sheet_df, column_mappings)
                if sheet_issues:
                    issues[sheet_name] = sheet_issues
        else:  # Single-sheet Excel file
            sheet_issues = validate_excel_sheet(df, column_mappings)
            if sheet_issues:
                issues["sheet_issues"] = sheet_issues

    return issues


# =================== File Hashing ===================


def compute_file_hash(file_name: str) -> str:
    """Simulates computing a file hash for tracking modifications or data integrity."""
    return hashlib.md5(file_name.encode()).hexdigest()


# =================== Centralized File Comparison ===================


def compare_hashes(
    context: Any,
    hash_to_compare: str,
    source_name: str = "context.db_data",
    target_name: Optional[str] = None,
) -> bool:
    """
    Compares two hashes (one from source_name and one from the given hash_to_compare).

    - context: The context in which the file is processed
    - hash_to_compare: The hash value that is being compared
    - source_name: The context or database from where the hash is taken (default is context.db_data)
    - target_name: The name of the file or record being compared
    """
    start_time = datetime.datetime.now()
    source_hash = _get_source_hash(context, source_name)
    is_modified = source_hash != hash_to_compare
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    logging.info(
        "Comparison for {}: {} (Time taken: {:.2f} seconds)".format(
            target_name,
            "Discrepancy found" if is_modified else "No discrepancy",
            duration,
        )
    )

    return is_modified


def _get_source_hash(context: Any, source_name: str) -> str:
    # Check if context has db_data attribute and return hash if available
    if hasattr(context, 'db_data') and source_name == "db_data":
        return context.db_data.get(
            "hash", ""
        )  # Return empty string if hash is not found

    # Check if resolved_issues exists in the context and return hash for the source_name
    elif hasattr(context, 'resolved_issues') and source_name in getattr(
        context, 'resolved_issues', {}
    ):
        return context.resolved_issues[source_name].get(
            "hash", ""
        )  # Return empty string if hash is not found

    # Check in historical_records
    elif source_name in historical_records:
        return historical_records[source_name].get(
            "hash", ""
        )  # Return empty string if hash is not found

    # If the source_name is not found in any of the options
    else:
        raise ValueError(
            "Source {0} not found in context or historical records.".format(source_name)
        )


def check_for_trailing_spaces(context: Any, file_name: str) -> None:
    """
    Check for trailing spaces in the columns and rows of the CSV or Excel file.
    Logs any issues found during the check.

    :param context: The context object that contains the necessary information.
    :param file_name: The name of the file to check for trailing spaces.
    :return: None
    """
    try:
        # Load the file into a DataFrame based on file type
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_name)
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file_name)
        else:
            raise ValueError("Unsupported file format for {0}".format(file_name))

        # Strip trailing spaces from column names
        df.columns = df.columns.str.strip()

        # Initialize list to track issues
        columns_with_trailing_spaces = []

        # Check for trailing spaces in each column (only for string/object columns)
        for column in df.columns:
            if df[column].dtype == object:  # Check only string columns
                # Strip trailing spaces from the column
                df[column] = df[column].str.strip()

                # Identify rows with trailing spaces in the column
                rows_with_trailing_spaces = df[column].str.contains(r'\s$', na=False)

                if rows_with_trailing_spaces.any():
                    columns_with_trailing_spaces.append(column)
                    # Log the number of rows with trailing spaces in the column
                    logging.warning(
                        "Trailing spaces detected in column '{0}' of file '{1}'. Rows affected: {2}".format(
                            column, file_name, rows_with_trailing_spaces.sum()
                        )
                    )

        # If no trailing spaces found, log that the file is clean
        if not columns_with_trailing_spaces:
            logging.info("No trailing spaces detected in file '{0}'.".format(file_name))

    except ValueError as e:
        # Handling specific ValueError
        logging.error("Error: {0}".format(str(e)))
        raise
    except Exception as e:
        # Handling any other general errors
        logging.error(
            "Error checking trailing spaces in file {0}: {1}".format(file_name, str(e))
        )
        raise ValueError(
            "Error checking trailing spaces in file {0}: {1}".format(file_name, str(e))
        )


# =================== Identifying Merged Cells in File and in Sheet ===================


def check_for_merged_cells_in_file(context):
    # type: (object) -> None
    """
    Checks for merged cells in the file (single or multi-sheet Excel files).

    :param context: Context object with attributes `file_name` and `df`
    :return: None
    """
    try:
        file_name_candidate = getattr(context, "file_name", None)  # type: object
        df = getattr(context, "df", None)  # type: object

        if not isinstance(file_name_candidate, six.string_types):
            raise ValueError("File name is not a valid string.")

        file_name = file_name_candidate  # type: str

        if df is None:
            raise ValueError("DataFrame is not defined in the context.")

        logging.info(
            "Starting to check for merged cells in file: {0}".format(file_name)
        )

        if file_name.endswith(".xlsx"):
            if isinstance(df, dict):  # Multi-sheet Excel file
                for sheet_name, sheet_df in df.items():
                    merged_rows_sheet = check_merged_cells_in_sheet(
                        sheet_df
                    )  # type: list
                    if merged_rows_sheet:
                        logging.warning(
                            "Merged cells found in sheet '{0}' of file '{1}': {2}".format(
                                sheet_name, file_name, merged_rows_sheet
                            )
                        )
                    else:
                        logging.info(
                            "No merged cells detected in sheet '{0}' of file '{1}'.".format(
                                sheet_name, file_name
                            )
                        )
            else:  # Single sheet
                merged_rows_single = check_merged_cells_in_sheet(df)  # type: list
                if merged_rows_single:
                    logging.warning(
                        "Merged cells found in file '{0}': {1}".format(
                            file_name, merged_rows_single
                        )
                    )
                else:
                    logging.info(
                        "No merged cells detected in file '{0}'.".format(file_name)
                    )
        else:
            logging.info(
                "File '{0}' is not an Excel file, skipping merged cells check.".format(
                    file_name
                )
            )

    except Exception as e:
        logging.error(
            "Error checking merged cells in file {0}: {1}".format(file_name, str(e))
        )
        raise ValueError(
            "Error checking merged cells in file {0}: {1}".format(file_name, str(e))
        )


def check_merged_cells_in_sheet(sheet_df):
    # type: (pd.DataFrame) -> list
    """
    Helper function to check for merged cells in a DataFrame (Excel sheet).

    :param sheet_df: The DataFrame representing the Excel sheet
    :return: A list of row indices where merged cells (NaN values) are detected in the first column
    """
    merged_cells = []  # type: list

    # Simulate checking for merged cells by identifying NaN values in the first column
    for index, row in sheet_df.iterrows():
        if pd.isna(row[0]):  # Assuming merged cells have NaN values in the first column
            merged_cells.append(index)

    return merged_cells
