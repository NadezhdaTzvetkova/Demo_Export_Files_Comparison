[![Allure Report](https://img.shields.io/badge/Allure-Report-blue?logo=allure&logoColor=white)](https://nadezhdatzvetkova.github.io/Demo_Export_Files_Comparison/)

# 🏦 Bank Export File Comparison Automation 📜

This repository contains **BDD (Behavior-Driven Development) and traditional Pytest automation tests** for **comparing banking export files (CSV/Excel)** between an **old banking system** and a **newly migrated system**.

---

## 🚀 Project Overview
The goal of this project is to:
- ✅ Validate that the **data in old and new exports match**.
- ✅ Detect **missing, extra, duplicated, or mismatched records**.
- ✅ Ensure that **file structures, formats, and encodings** are consistent.
- ✅ Identify **performance bottlenecks** with large transaction volumes.
- ✅ Automate the **download of large test datasets from Google Drive**.
- ✅ Secure **commit signing using GPG** for Git authentication.
- ✅ Provide **detailed, actionable reports** through Allure.
- ✅ Support **parallel test execution** for performance and scalability.
- ✅ **Auto-publish Allure Reports** to GitHub Pages for easy access.

---

## 📂 Project Structure
```text
Demo_Export_Files_Comparison/
│── .github/
│   └── workflows/               # GitHub Actions CI workflow
│── config/                     # Configuration files (e.g., file mappings)
│── features/                   # BDD test scenarios
│   ├── data_validation_tests/      # Tests for data accuracy
│   ├── duplicate_and_integrity_tests/  # Duplicate/mismatch checks
│   ├── edge_case_tests/            # Tests for edge and null cases
│   ├── performance_tests/          # Performance and load testing
│   ├── structural_tests/           # File structure and format checks
│   └── regression_tests/           # Regression tests for previous bugs
│── test_data/                  # Sample CSV & Excel files for testing
│── scripts/                    # Python scripts for test execution
│   ├── download_large_files.py     # Downloads large test datasets
│   ├── run_tests.py                # Executes all tests
│   └── install_dependencies.py     # Installs dependencies
│── utils/                      # Utility/helper functions
│── behave.ini                  # Behave configuration file
│── requirements.txt            # Python dependencies
│── README.md                   # Project documentation
```

---

## 🛠️ Setup Instructions

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/NadezhdaTzvetkova/Demo_Export_Files_Comparison.git
cd Demo_Export_Files_Comparison
```

### **2️⃣ Set Up a Virtual Environment**
```sh
python -m venv .venv
source .venv/bin/activate  # For macOS/Linux
.venv\Scripts\activate     # For Windows
```

---

## 🔧 Install Dependencies

### **3️⃣ Install Required Python Packages**
```sh
pip install -r requirements.txt
```

### **4️⃣ Install Git LFS (For Large Files)**
```sh
git lfs install
git lfs pull
```

---

## 📅 Automatic Download of Large Test Files
This project requires large test datasets, which are **stored in Google Drive** and automatically downloaded before test execution.

### **🔗 Setting Up Google Drive API**
1. **Enable the Google Drive API** in [Google Cloud Console](https://console.cloud.google.com/apis/library/drive.googleapis.com).
2. **Create a Service Account** and download `credentials.json`.
3. **Move `credentials.json` to the `scripts/` folder.**
4. **Run the script to download files:**
   ```sh
   python scripts/download_large_files.py
   ```
   This script:
   - Authenticates with Google Drive
   - Lists all files in the shared testing folder
   - Downloads them into `test_data/`
   - Skips files that are already downloaded

---

## 🔑 Secure Git Commits with GPG Signing
All commits must be **signed using GPG**.

### **5️⃣ Generate and Configure GPG Key**
```sh
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long
```
Copy the **GPG key ID** and configure Git:
```sh
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
```

Test it:
```sh
echo "test" > test.txt
git add test.txt
git commit -S -m "Test GPG signing"
```
If successful, push changes:
```sh
git push origin main
```

---

## 🏃‍♂️ Running Tests

### **6️⃣ Run All Behave Tests**
```sh
behave
```

### **Run Specific Test Categories**
```sh
behave --tags=data_validation
behave --tags=performance_tests
behave --tags=regression
```

### **7️⃣ Run All Pytest Tests (Parallelized)**
```sh
pytest -n auto
```

---

## 📄 BDD Test Features
| 📂 Folder                         | 📜 Test Coverage |
|----------------------------------|------------------|
| `data_validation_tests/`         | Data accuracy, formatting, encoding |
| `duplicate_and_integrity_tests/` | Detects duplicate transactions, data mismatches |
| `edge_case_tests/`               | Handles missing, extreme, and zero-value cases |
| `performance_tests/`             | Measures processing speed & concurrency |
| `structural_tests/`              | Verifies headers, column orders, and structures |
| `regression_tests/`              | Ensures previous issues do not reoccur |

---

## 📊 Sample Test Data
| **Test Scenario**   | **CSV File**                          | **Excel File**                         |
|---------------------|----------------------------------------|----------------------------------------|
| Baseline Validation | `bank_export_baseline_test.csv`       | `bank_export_baseline_test.xlsx`       |
| Negative Values     | `bank_export_negative_values_test.csv`| `bank_export_negative_values_test.xlsx`|
| Missing Values      | `bank_export_missing_values_test.csv` | `bank_export_missing_values_test.xlsx` |
| Extra Columns       | `bank_export_extra_columns_test.csv`  | `bank_export_extra_columns_test.xlsx`  |
| Reordered Columns   | `bank_export_reordered_columns_test.csv`| `bank_export_reordered_columns_test.xlsx`|

---

## ⚡️ Continuous Integration & Allure Reporting
Powered by **GitHub Actions**, the project supports full test automation.

### 🦢 CI Features
- ✅ **Matrix Testing** across Python 3.9, 3.10, 3.11
- 🌀 **Parallel Testing** via `pytest-xdist`
- 📜 **BDD with Behave** and traditional tests with **pytest**
- 📊 **Code Coverage** tracking via `coverage.py` + Codecov
- 📚 **Allure Reports** generated and uploaded as CI artifacts
- 🔔 **Slack Notifications** for test results
- 🌐 **GitHub Pages Deployment** for public Allure report access

### 📊 Allure Reports
The pipeline collects test results for both Behave and Pytest and publishes them as beautiful, interactive HTML reports.

#### ✅ Features:
- Behave + Pytest combined reports
- Downloadable from the **Actions tab**
- Auto-published to **GitHub Pages** for easy access

#### 🗕️ View the Report:
1. Open the **Actions** tab
2. Click the latest workflow run
3. Download the `allure-html` artifact

🗕️ Or view live: [Live Allure Report](https://nadezhdatzvetkova.github.io/Demo_Export_Files_Comparison)

---

## 🏆 Contribution Guide
🔹 **Want to contribute? Follow these steps!**
1. **Open an issue** for bugs or enhancements.
2. **Fork the repository** and create a new branch.
3. **Follow the BDD test structure** for consistency.
4. **Submit a pull request (PR)** with a clear description.

---

## 🔗 Useful Links
📖 [Behave Docs](https://behave.readthedocs.io/en/latest/)
📖 [Pytest Docs](https://docs.pytest.org/)
📊 [Allure Docs](https://docs.qameta.io/allure/)
📌 [Google Drive API Setup](https://console.cloud.google.com/apis/library/drive.googleapis.com)

---

## 💡 Maintained by: **Nadezhda Nikolova**
🚀 Happy testing! 🎯
