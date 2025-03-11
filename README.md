# 🏦 Bank Export File Comparison Automation 📝

This repository contains **BDD (Behavior-Driven Development) automation tests** for **comparing banking export files (CSV/Excel)** from an **old banking system** to a **newly migrated system**.

## 🚀 Project Overview
The goal of this project is to:
- ✅ Validate that the **data in old and new exports match**.
- ✅ Detect **missing, extra, duplicated, or mismatched records**.
- ✅ Ensure that **file structures, formats, and encodings** are consistent.
- ✅ Identify **performance bottlenecks** with large transaction volumes.

## 📂 Project Structure
Demo_Export_Files_Comparison/ │── config/ # Configuration files (e.g., file mappings) │── features/ # BDD test scenarios │ │── data_validation_tests/ # Tests for data accuracy │ │── duplicate_and_integrity_tests/ # Tests for duplicates and mismatches │ │── edge_case_tests/ # Tests for missing values, extreme data │ │── performance_tests/ # Performance and load testing │ │── structural_tests/ # File structure and format checks │ │── regression_tests/ # Regression tests for previous fixes │── test_data/ # Sample CSV & Excel files for testing │── scripts/ # Python scripts for test execution │── utils/ # Utility functions │── behave.ini # Behave configuration file │── requirements.txt # Python dependencies │── README.md # Project documentation

## 🛠️ Setup Instructions
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/NadezhdaTzvetkova/Demo_Export_Files_Comparison.git
cd Demo_Export_Files_Comparison

2️⃣ Set Up a Virtual Environment
python -m venv .venv
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Tests Using Behave
behave  # Runs all tests
behave --tags=data_validation  # Runs only data validation tests
behave --tags=performance_tests  # Runs only performance tests

📄 BDD Test Features
Folder	Test Coverage
data_validation_tests/	Data accuracy, formatting, encoding
duplicate_and_integrity_tests/	Detects duplicate transactions, data mismatches
edge_case_tests/	Handles missing, extreme, and zero-value cases
performance_tests/	Measures processing speed & concurrency
structural_tests/	Verifies headers, column orders, and structures
regression_tests/	Ensures previous issues do not reoccur

📊 Sample Test Data
Test files used for validation:

Baseline Test: bank_export_baseline_test.xlsx / bank_export_baseline_test.csv
Negative Values: bank_export_negative_values_test.xlsx / bank_export_negative_values_test.csv
Missing Values: bank_export_missing_values_test.xlsx / bank_export_missing_values_test.csv
Extra Columns: bank_export_extra_columns_test.xlsx / bank_export_extra_columns_test.csv
Reordered Columns: bank_export_reordered_columns_test.xlsx / bank_export_reordered_columns_test.csv

⚡ Continuous Integration (CI/CD)
Run tests automatically with GitHub Actions (future setup).
Generate test reports for each execution.

🏆 Contribution Guide
Open an issue for bugs or enhancements.
Follow BDD test structure for consistency.
Submit PRs with clear descriptions.

🔗 Useful Links
Behave Documentation: https://behave.readthedocs.io/en/latest/
Python Testing Best Practices

💡 Maintained by: Nadezhda Nikolova
🚀 Happy testing! 🎯


---

### **📌 Next Steps**
1️⃣ **Create and commit the `README.md` file**  
2️⃣ **Push it to GitHub**:
```sh
git add README.md
git commit -m "Added project documentation in README.md"
git push origin main