import pandas as pd
import numpy as np

# Define transaction uniqueness test files
uniqueness_test_files = [
    ("transactions_2022.csv", 1_000_000),  # 1 million unique transactions
    (
        "transactions_2023.parquet",
        5_000_000,
    ),  # 5 million unique transactions (stored as Parquet)
]


def generate_transaction_data(file_name, transaction_count):
    """Generate transaction data ensuring all references are unique."""

    # Create unique transaction reference IDs
    transaction_references = np.arange(1, transaction_count + 1, dtype=int)
    np.random.shuffle(transaction_references)  # Shuffle to avoid sequential patterns

    # Create transaction data
    data = pd.DataFrame(
        {
            "Transaction_ID": transaction_references,
            "Amount": np.random.uniform(10, 5000, transaction_count).round(2),
            "Currency": np.random.choice(["USD", "EUR", "GBP"], transaction_count),
            "Timestamp": pd.date_range(
                start="2022-01-01", periods=transaction_count, freq="min"
            ),
            "Status": np.random.choice(
                ["Completed", "Pending", "Failed"],
                transaction_count,
                p=[0.9, 0.08, 0.02],
            ),
        }
    )

    # Save CSV directly
    if file_name.endswith(".csv"):
        data.to_csv(file_name, index=False)
        print(f"✅ File {file_name} generated successfully.")
        return

    # Save large files as Parquet (Excel Alternative)
    elif file_name.endswith(".parquet"):
        data.to_parquet(file_name, index=False, engine="pyarrow")
        print(f"✅ File {file_name} generated successfully as a Parquet file.")


# Generate files for transaction uniqueness scenario
for file_name, transaction_count in uniqueness_test_files:
    generate_transaction_data(file_name, transaction_count)

print("\n🎉 All transaction uniqueness test files generated successfully!")
