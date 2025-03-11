import pandas as pd
import os


def compare_csv_files(file1: str, file2: str, ignore_order=True):
    """
    Compares two CSV files for differences in column headers and data.
    :param file1: Path to the first CSV file.
    :param file2: Path to the second CSV file.
    :param ignore_order: If True, ignores row order differences.
    :return: Dictionary with comparison results.
    """
    print(f"[INFO] Comparing CSV files: {file1} vs {file2}")
    if not os.path.exists(file1) or not os.path.exists(file2):
        print(
            f"[ERROR] One or both CSV files do not exist. File1 Exists: {os.path.exists(file1)}, File2 Exists: {os.path.exists(file2)}")
        return {"error": "One or both files do not exist", "file1_exists": os.path.exists(file1),
                "file2_exists": os.path.exists(file2)}

    df1 = pd.read_csv(file1, dtype=str)
    df2 = pd.read_csv(file2, dtype=str)

    print("[INFO] Checking CSV column headers...")
    if list(df1.columns) != list(df2.columns):
        print("[ERROR] CSV column headers do not match!")
        return {"error": "Column headers do not match", "file1_columns": df1.columns.tolist(),
                "file2_columns": df2.columns.tolist()}

    if ignore_order:
        print("[INFO] Sorting CSV files for comparison...")
        df1 = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
        df2 = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    print("[INFO] Comparing CSV data rows...")
    if not df1.equals(df2):
        diff_rows = df1.compare(df2, keep_equal=False)
        print("[ERROR] CSV data mismatch found!")
        return {"error": "Data mismatch", "differences": diff_rows.to_dict()}

    print("[SUCCESS] CSV files are identical!")
    return {"status": "Match", "message": "The CSV files are identical"}


def compare_excel_files(file1: str, file2: str, sheet_name=None, ignore_order=True):
    """
    Compares two Excel files for differences in column headers and data.
    :param file1: Path to the first Excel file.
    :param file2: Path to the second Excel file.
    :param sheet_name: Name of the sheet to compare (default: first sheet).
    :param ignore_order: If True, ignores row order differences.
    :return: Dictionary with comparison results.
    """
    print(f"[INFO] Comparing Excel files: {file1} vs {file2}")
    if not os.path.exists(file1) or not os.path.exists(file2):
        print(
            f"[ERROR] One or both Excel files do not exist. File1 Exists: {os.path.exists(file1)}, File2 Exists: {os.path.exists(file2)}")
        return {"error": "One or both files do not exist", "file1_exists": os.path.exists(file1),
                "file2_exists": os.path.exists(file2)}

    df1 = pd.read_excel(file1, sheet_name=sheet_name or 0, dtype=str)
    df2 = pd.read_excel(file2, sheet_name=sheet_name or 0, dtype=str)

    print("[INFO] Checking Excel column headers...")
    if list(df1.columns) != list(df2.columns):
        print("[ERROR] Excel column headers do not match!")
        return {"error": "Column headers do not match", "file1_columns": df1.columns.tolist(),
                "file2_columns": df2.columns.tolist()}

    if ignore_order:
        print("[INFO] Sorting Excel files for comparison...")
        df1 = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
        df2 = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    print("[INFO] Comparing Excel data rows...")
    if not df1.equals(df2):
        diff_rows = df1.compare(df2, keep_equal=False)
        print("[ERROR] Excel data mismatch found!")
        return {"error": "Data mismatch", "differences": diff_rows.to_dict()}

    print("[SUCCESS] Excel files are identical!")
    return {"status": "Match", "message": "The Excel files are identical"}


if __name__ == "__main__":
    print("[INFO] Starting file comparison...")

    file1_csv = "data/bank_export_csv_format_validation_params.csv"
    file2_csv = "data/bank_export_csv_format_validation_params_reference.csv"

    file1_excel = "data/bank_export_excel_format_validation_params.xlsx"
    file2_excel = "data/bank_export_excel_format_validation_params_reference.xlsx"

    print("[INFO] Checking CSV files...")
    csv_result = compare_csv_files(file1_csv, file2_csv)
    print("[RESULT] CSV Comparison Result:")
    print(csv_result)

    print("[INFO] Checking Excel files...")
    excel_result = compare_excel_files(file1_excel, file2_excel)
    print("[RESULT] Excel Comparison Result:")
    print(excel_result)

    print("[INFO] File comparison completed.")
