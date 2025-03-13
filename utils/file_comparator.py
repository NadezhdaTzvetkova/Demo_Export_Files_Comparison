import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(
    filename="logs/file_comparator.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def load_csv(file_path: str):
    """Loads a CSV file and returns a DataFrame."""
    try:
        return pd.read_csv(file_path, dtype=str, keep_default_na=False)
    except Exception as e:
        logging.error(f"Error loading CSV file {file_path}: {e}")
        return None

def load_excel(file_path: str, sheet_name=None):
    """Loads an Excel file and returns a DataFrame."""
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name or 0, dtype=str, keep_default_na=False)
    except Exception as e:
        logging.error(f"Error loading Excel file {file_path}: {e}")
        return None

def compare_csv_files(file1: str, file2: str, ignore_order=True):
    """
    Compares two CSV files for differences in column headers and data.
    """
    logging.info(f"Comparing CSV files: {file1} vs {file2}")

    if not os.path.exists(file1) or not os.path.exists(file2):
        logging.error(f"One or both CSV files do not exist: {file1}, {file2}")
        return {"error": "One or both files do not exist"}

    df1, df2 = load_csv(file1), load_csv(file2)
    if df1 is None or df2 is None:
        return {"error": "Failed to load one or both files"}

    # Compare headers
    if set(df1.columns) != set(df2.columns):
        logging.error(f"CSV column headers do not match!")
        return {"error": "Column headers do not match", "file1_columns": list(df1.columns), "file2_columns": list(df2.columns)}

    # Normalize order
    if ignore_order:
        logging.info("Sorting CSV files for comparison...")
        df1, df2 = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True), df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    # Compare data
    logging.info("Comparing CSV data rows...")
    diff = df1.compare(df2, keep_equal=False) if not df1.equals(df2) else None
    if diff is not None and not diff.empty:
        logging.error("CSV data mismatch found!")
        return {"error": "Data mismatch", "differences": diff.to_dict()}

    logging.info("CSV files are identical!")
    return {"status": "Match", "message": "The CSV files are identical"}

def compare_excel_files(file1: str, file2: str, sheet_name=None, ignore_order=True):
    """
    Compares two Excel files for differences in column headers and data.
    """
    logging.info(f"Comparing Excel files: {file1} vs {file2}")

    if not os.path.exists(file1) or not os.path.exists(file2):
        logging.error(f"One or both Excel files do not exist: {file1}, {file2}")
        return {"error": "One or both files do not exist"}

    df1, df2 = load_excel(file1, sheet_name), load_excel(file2, sheet_name)
    if df1 is None or df2 is None:
        return {"error": "Failed to load one or both files"}

    # Compare headers
    if set(df1.columns) != set(df2.columns):
        logging.error(f"Excel column headers do not match!")
        return {"error": "Column headers do not match", "file1_columns": list(df1.columns), "file2_columns": list(df2.columns)}

    # Normalize order
    if ignore_order:
        logging.info("Sorting Excel files for comparison...")
        df1, df2 = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True), df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    # Compare data
    logging.info("Comparing Excel data rows...")
    diff = df1.compare(df2, keep_equal=False) if not df1.equals(df2) else None
    if diff is not None and not diff.empty:
        logging.error("Excel data mismatch found!")
        return {"error": "Data mismatch", "differences": diff.to_dict()}

    logging.info("Excel files are identical!")
    return {"status": "Match", "message": "The Excel files are identical"}

if __name__ == "__main__":
    logging.info("Starting file comparison...")

    test_files = {
        "csv": ("test_data/csv_files/bank_export_baseline_test.csv", "test_data/csv_files/bank_export_reordered_columns_test.csv"),
        "excel": ("test_data/excel_files/bank_export_baseline_test.xlsx", "test_data/excel_files/bank_export_reordered_columns_test.xlsx"),
    }

    logging.info("Checking CSV files...")
    csv_result = compare_csv_files(*test_files["csv"])
    logging.info(f"CSV Comparison Result: {csv_result}")

    logging.info("Checking Excel files...")
    excel_result = compare_excel_files(*test_files["excel"])
    logging.info(f"Excel Comparison Result: {excel_result}")

    logging.info("File comparison completed.")
