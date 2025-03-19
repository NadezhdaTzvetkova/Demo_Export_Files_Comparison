import os

def get_feature_files_directory():
    """Automatically detect the project's feature files directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    feature_files_dir = os.path.join(project_root, "features")

    if not os.path.exists(feature_files_dir):
        print(f"⚠️ Warning: Feature files directory '{feature_files_dir}' not found.")
    return feature_files_dir


def fix_gherkin_indentation(file_path):
    """Fix indentation while ensuring the integrity of all Gherkin structures."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    previous_was_blank = False
    inside_table = False
    inside_examples = False

    for index, line in enumerate(lines):
        stripped = line.strip()

        # Remove all --- separators (Behave does not support them)
        if stripped == "---":
            continue

        # Ensure a blank line before Scenario/Scenario Outline
        if stripped.startswith(("Scenario", "Scenario Outline")):
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")  # Add blank line before Scenario
            formatted_lines.append(stripped)
            previous_was_blank = False
            inside_examples = False  # Reset Examples flag
            continue

        # Ensure Examples: is properly preserved and NOT followed by a blank line
        if stripped.startswith("Examples:"):
            inside_examples = True
            formatted_lines.append("")
            formatted_lines.append(stripped)
            previous_was_blank = False
            continue

        # Ensure correct table formatting
        if inside_examples and stripped.startswith("|"):
            inside_table = True
        else:
            inside_table = False

        if inside_table:
            # Ensure each row starts and ends with '|'
            if not stripped.endswith("|"):
                stripped += " |"
            if not stripped.startswith("|"):
                stripped = "| " + stripped
            formatted_lines.append(stripped)
            previous_was_blank = False
            continue

        # Remove excessive blank lines except where required
        if not stripped:
            if previous_was_blank or inside_examples:
                continue  # Skip consecutive blank lines
            previous_was_blank = True
            formatted_lines.append("")  # Keep a single blank line
            continue

        # Ensure no blank lines between tags and Scenario/Scenario Outline
        if stripped.startswith("@"):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove unnecessary blank line before a tag
            formatted_lines.append(stripped)
            previous_was_blank = False
            continue

        # Ensure Given, When, Then are preserved
        if stripped.startswith(("Given", "When", "Then", "And", "But")):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove blank line between steps
            formatted_lines.append("\t" + stripped)
            previous_was_blank = False
            continue

        # Preserve everything else as is
        formatted_lines.append(stripped)
        previous_was_blank = False  # Reset blank line tracker

    # Ensure the file ends with a single newline
    if formatted_lines and formatted_lines[-1] != "":
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
        "One blank line before Scenario/Scenario Outline, but none between Examples: and its table."
    )


if __name__ == "__main__":
    feature_files_dir = get_feature_files_directory()
    process_feature_files(feature_files_dir)
