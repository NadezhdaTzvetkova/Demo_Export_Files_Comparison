import pandas as pd
import numpy as np

# Install dependencies if missing
try:
    pass
except ImportError:
    print("❌ Missing required libraries. Install them using:")
    print("   pip install pyarrow openpyxl pandas")
    exit(1)

# Define missing test files
missing_test_files = [
    ("database_2018_2022.csv", 500_000),
    ("database_2023_2024.csv", 200_000),
    ("batch_2018_2022.parquet", 1_500_000),
    ("batch_2023_2024.parquet", 2_000_000),
    ("transactions_2019.csv", 200_000, "duplicate"),
    ("transactions_2021.xlsx", 150_000, "missing"),
    ("performance_2015_2020.csv", 3_000_000),
    ("performance_2021_2023.parquet", 5_000_000),
]

EXCEL_MAX_ROWS = 1_048_576


def generate_transaction_data(file_name, transaction_count, issue_type=None):
    """Generate transaction data for different test cases."""

    # Create transaction reference IDs
    transaction_references = np.arange(1, transaction_count + 1, dtype=int)

    if issue_type == "duplicate":
        transaction_references[:10_000] = transaction_references[
            :10_000
        ]  # Duplicates in first 10K rows

    if issue_type == "missing":
        transaction_references = transaction_references.astype(
            float
        )  # ✅ Convert to float before NaN
        transaction_references[:10_000] = np.nan  # ✅ No more error

    np.random.shuffle(transaction_references)  # Shuffle to avoid sequential patterns

    # Create transaction data
    data = pd.DataFrame(
        {
            "Transaction_ID": transaction_references,
            "Amount": np.random.uniform(10, 5000, transaction_count).round(2),
            "Currency": np.random.choice(["USD", "EUR", "GBP"], transaction_count),
            "Timestamp": pd.date_range(
                start="2015-01-01", periods=transaction_count, freq="min"
            ),
            "Status": np.random.choice(
                ["Completed", "Pending", "Failed"],
                transaction_count,
                p=[0.9, 0.08, 0.02],
            ),
        }
    )

    # Save CSV
    if file_name.endswith(".csv"):
        data.to_csv(file_name, index=False)
        print(f"✅ File {file_name} generated successfully.")

    # Save Excel
    elif file_name.endswith(".xlsx"):
        with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
            sheet_count = 1
            for start_row in range(0, transaction_count, EXCEL_MAX_ROWS):
                end_row = min(start_row + EXCEL_MAX_ROWS, transaction_count)
                sheet_name = f"Sheet_{sheet_count}"

                subset = data.iloc[start_row:end_row].copy()
                subset.reset_index(drop=True, inplace=True)

                subset.to_excel(writer, index=False, sheet_name=sheet_name)
                sheet_count += 1

        print(
            f"✅ File {file_name} generated successfully with {sheet_count - 1} sheets."
        )

    # Save Parquet
    elif file_name.endswith(".parquet"):
        data.to_parquet(file_name, index=False, engine="pyarrow")
        print(f"✅ File {file_name} generated successfully as a Parquet file.")


# Generate missing test files
for file_info in missing_test_files:
    if len(file_info) == 2:
        generate_transaction_data(file_info[0], file_info[1])
    else:
        generate_transaction_data(file_info[0], file_info[1], issue_type=file_info[2])

print("\n🎉 All missing test files generated successfully!")
