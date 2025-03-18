import pandas as pd
import os
import logging
import json

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "file_comparator.log"),
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

def compare_files(file1: str, file2: str, file_type="csv", sheet_name=None, ignore_order=True):
    """
    Compares two CSV or Excel files and logs results.
    """
    logging.info(f"Comparing {file_type.upper()} files: {file1} vs {file2}")

    if not os.path.exists(file1) or not os.path.exists(file2):
        logging.error(f"One or both files do not exist: {file1}, {file2}")
        return {"error": "One or both files do not exist"}

    df1 = load_csv(file1) if file_type == "csv" else load_excel(file1, sheet_name)
    df2 = load_csv(file2) if file_type == "csv" else load_excel(file2, sheet_name)

    if df1 is None or df2 is None:
        return {"error": "Failed to load one or both files"}

    # Compare column headers
    if set(df1.columns) != set(df2.columns):
        logging.error(f"{file_type.upper()} column headers do not match!")
        return {
            "error": "Column headers do not match",
            "file1_columns": list(df1.columns),
            "file2_columns": list(df2.columns),
        }

    # Normalize order if needed
    if ignore_order:
        logging.info("Sorting files for comparison...")
        df1 = df1.sort_values(by=df1.columns.tolist(), ignore_index=True)
        df2 = df2.sort_values(by=df2.columns.tolist(), ignore_index=True)

    # Compare data
    logging.info("Comparing data rows...")
    if not df1.equals(df2):
        diff = df1.compare(df2, keep_equal=False)
        logging.error(f"{file_type.upper()} data mismatch found!")
        return {"error": "Data mismatch", "differences": diff.to_dict()}

    logging.info(f"{file_type.upper()} files are identical!")
    return {"status": "Match", "message": f"The {file_type.upper()} files are identical"}

if __name__ == "__main__":
    logging.info("Starting automated file comparison...")

    config_path = "config/test_file_mappings.json"
    os.makedirs("reports", exist_ok=True)

    try:
        with open(config_path, "r") as f:
            test_files = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load test file mappings: {e}")
        exit(1)

    results = {}
    for test, files in test_files.items():
        file1, file2 = files["old_system"], files["new_system"]
        file_type = "csv" if file1.endswith(".csv") else "excel"
        result = compare_files(file1, file2, file_type=file_type, sheet_name=files.get("sheet_name"))
        results[test] = result
        logging.info(f"[RESULT] {test}: {result}")

    output_path = "reports/comparison_results.json"
    with open(output_path, "w") as outfile:
        json.dump(results, outfile, indent=4)

    logging.info("File comparison completed.")
