import json
from behave import given, when, then
from test_data.utils.file_comparator import compare_files

@given('I have export file mappings')
def step_given_file_mappings(context):
    with open("config/test_file_mappings.json", "r") as f:
        context.test_files = json.load(f)

@when('I compare files for "{test_name}"')
def step_when_compare_files(context, test_name):
    test_data = context.test_files.get(test_name)
    if not test_data:
        context.result = {"error": "Test case not found"}
        return

    file1, file2 = test_data["old_system"], test_data["new_system"]
    file_type = "csv" if file1.endswith(".csv") else "excel"
    context.result = compare_files(file1, file2, file_type=file_type, sheet_name=test_data.get("sheet_name"))

@then('the files should be identical')
def step_then_files_should_match(context):
    assert context.result.get("status") == "Match", f"Mismatch found: {context.result}"
