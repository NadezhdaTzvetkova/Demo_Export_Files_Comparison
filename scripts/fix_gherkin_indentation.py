import os
import re


def get_feature_files_directory():
    """Automatically detect the project's feature files directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    feature_files_dir = os.path.join(project_root, "features")

    if not os.path.exists(feature_files_dir):
        print(f"⚠️ Warning: Feature files directory '{feature_files_dir}' not found.")
    return feature_files_dir


def validate_table_format(table_lines):
    """Validate and fix formatting issues in Gherkin Examples tables."""
    fixed_lines = []
    max_columns = 0

    for line in table_lines:
        # Remove spaces between values instead of pipes
        line = re.sub(r"\s+\|\s+", "|", line.strip())

        # Ensure the row starts and ends with a "|"
        if not line.startswith("|"):
            line = "|" + line
        if not line.endswith("|"):
            line = line + "|"

        # Count the number of columns in the row
        column_count = line.count("|") - 1  # Subtract 1 to get actual columns
        max_columns = max(max_columns, column_count)
        fixed_lines.append(line)

    # Ensure all rows have the same number of columns
    for i, line in enumerate(fixed_lines):
        current_columns = line.count("|") - 1
        if current_columns < max_columns:
            missing_pipes = max_columns - current_columns
            fixed_lines[i] = line[:-1] + " |" * missing_pipes + "|"

    return fixed_lines


def fix_gherkin_indentation(file_path):
    """Fix indentation, ensure spacing rules, and remove unsupported elements."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    previous_was_blank = False
    inside_examples = False
    table_lines = []

    for line in lines:
        stripped = line.strip()

        # Remove "---" separators (Behave does not support them)
        if stripped == "---":
            continue

        # Remove excessive blank lines
        if not stripped:
            if previous_was_blank:
                continue  # Skip consecutive blank lines
            previous_was_blank = True
            formatted_lines.append("")  # Keep a single blank line
            continue

        # Ensure exactly one blank line after Feature
        if stripped.startswith("Feature"):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove last empty line if before Feature
            formatted_lines.append(stripped)
            formatted_lines.append("")  # Ensure exactly one blank line after Feature
            previous_was_blank = True
            continue

        # Ensure no blank lines between tags and Scenario/Scenario Outline
        if stripped.startswith("@"):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove unnecessary blank line before a tag
            formatted_lines.append(stripped)
            previous_was_blank = False
            continue

        # Ensure a blank line before Scenario/Scenario Outline
        if stripped.startswith(("Scenario", "Scenario Outline")):
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")  # Add a blank line before Scenario
            formatted_lines.append(stripped)
            previous_was_blank = False
            continue

        # Ensure a blank line after Examples:
        if stripped.startswith("Examples:"):
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")  # Ensure a blank line before Examples
            formatted_lines.append(stripped)
            formatted_lines.append("")  # Ensure a blank line after Examples:
            inside_examples = True
            table_lines = []  # Reset table content tracking
            previous_was_blank = True
            continue

        # Process table lines inside Examples
        if inside_examples and stripped.startswith("|"):
            table_lines.append(stripped)
            continue

        # If leaving Examples, process the table and append it
        if inside_examples and not stripped.startswith("|"):
            formatted_lines.extend(validate_table_format(table_lines))
            inside_examples = False  # Exit table processing

        # Given, When, Then → Indented by 1 tab
        if stripped.startswith(("Given", "When", "Then")):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove blank line between steps
            formatted_lines.append("\t" + stripped)

        # And, But → Indented by 2 tabs
        elif stripped.startswith(("And", "But")):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove blank line between steps
            formatted_lines.append("\t\t" + stripped)

        # Preserve everything else as is
        else:
            formatted_lines.append(stripped)

        previous_was_blank = False  # Reset blank line tracker

    # Ensure the last table is processed
    if inside_examples:
        formatted_lines.extend(validate_table_format(table_lines))

    # Ensure the file ends with a single newline
    if formatted_lines[-1] != "":
        formatted_lines.append("")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(formatted_lines))


def process_feature_files(directory):
    """Process all .feature files and fix indentation."""
    if not os.path.exists(directory):
        print("🚨 Feature files directory not found! Check your project structure.")
        return

    feature_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.endswith(".feature")
    ]

    if not feature_files:
        print("⚠️ No .feature files found to process.")
        return

    for file in feature_files:
        fix_gherkin_indentation(file)

    print(
        "✅ Gherkin indentation fixed successfully! "
        "One blank line after Feature, before Scenario/Scenario Outline, and after Examples!"
    )


if __name__ == "__main__":
    feature_files_dir = get_feature_files_directory()
    process_feature_files(feature_files_dir)
