import pandas as pd
import numpy as np

# Define batch processing files
batch_processing_files = [
    ("batch_2018_2022.csv", 500000, True),  # High severity (includes duplicates)
    ("batch_2023_2024.xlsx", 500000, False),  # Medium severity (unique references)
]


def generate_transaction_data(file_name, transaction_count, has_duplicates):
    """Generate transaction data ensuring uniqueness or introducing duplicates."""

    # Create unique transaction IDs
    transaction_references = np.arange(1, transaction_count + 1)
    np.random.shuffle(transaction_references)

    # Introduce duplicates if required
    if has_duplicates:
        duplicate_indices = np.random.choice(transaction_count, size=int(transaction_count * 0.001), replace=False)
        transaction_references[duplicate_indices] = transaction_references[np.random.choice(duplicate_indices)]

    # Create the transaction data
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


# Generate files for batch processing scenario
for file_name, transaction_count, has_duplicates in batch_processing_files:
    generate_transaction_data(file_name, transaction_count, has_duplicates)

print("Batch processing files generated successfully.")
