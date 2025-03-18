import pandas as pd
import numpy as np

# Define performance testing files
performance_testing_files = [
    ("performance_2015_2020.csv", 100000),  # 100 files/hour
    ("performance_2021_2023.xlsx", 500000),  # 500 files/hour
]


def generate_transaction_data(file_name, transaction_count):
    """Generate large transaction data files for performance testing."""

    # Create unique transaction reference IDs
    transaction_references = np.arange(1, transaction_count + 1)
    np.random.shuffle(transaction_references)

    # Create transaction data
    data = pd.DataFrame({
        "Transaction_ID": transaction_references,
        "Amount": np.random.uniform(10, 5000, transaction_count).round(2),
        "Currency": np.random.choice(["USD", "EUR", "GBP"], transaction_count),
        "Timestamp": pd.date_range(start="2022-01-01", periods=transaction_count, freq="min"),
        "Status": np.random.choice(["Completed", "Pending", "Failed"], transaction_count, p=[0.9, 0.08, 0.02]),
    })

    # Save the file
    if file_name.endswith(".csv"):
        data.to_csv(file_name, index=False)
    else:
        data.to_excel(file_name, index=False, engine="openpyxl")


# Generate files for performance testing scenario
for file_name, transaction_count in performance_testing_files:
    generate_transaction_data(file_name, transaction_count)

print("Performance testing files generated successfully.")
