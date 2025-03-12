import os

def get_feature_files_directory():
    """Automatically detect the project's feature files directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    feature_files_dir = os.path.join(project_root, "features")

    if not os.path.exists(feature_files_dir):
        print(f"⚠️ Warning: Feature files directory '{feature_files_dir}' not found.")
    return feature_files_dir


def fix_gherkin_indentation(file_path):
    """Fix indentation and remove extra blank lines from Gherkin feature files."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    inside_scenario = False
    previous_was_blank = False  # Track blank lines to remove unnecessary ones

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Remove excessive blank lines (before Feature, Scenario, and Steps)
        if stripped == "":
            if previous_was_blank:
                continue  # Skip consecutive blank lines
            previous_was_blank = True
            continue  # Skip all empty lines except necessary ones

        # Ensure no blank line exists before Feature, Scenario, Scenario Outline
        if stripped.startswith(("Feature", "Scenario", "Scenario Outline")):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove the last empty line if it's before these
            formatted_lines.append(stripped)
            inside_scenario = stripped.startswith(("Scenario", "Scenario Outline"))  # Enable scenario tracking
            previous_was_blank = False
            continue

        # Ensure no blank line exists between Tags (@) and Feature or Scenario
        if stripped.startswith("@"):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove the last empty line before a tag
            formatted_lines.append(stripped)
            previous_was_blank = False
            continue

        # Given, When, Then → Indented by 1 tab
        if stripped.startswith(("Given", "When", "Then")):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove any empty line between steps
            formatted_lines.append("\t" + stripped)

        # And, But → Indented by 2 tabs
        elif stripped.startswith(("And", "But")):
            if formatted_lines and formatted_lines[-1] == "":
                formatted_lines.pop()  # Remove any empty line between steps
            formatted_lines.append("\t\t" + stripped)

        # Preserve everything else as is
        else:
            formatted_lines.append(stripped)

        previous_was_blank = False  # Reset blank line tracker

    # Ensure the file ends with a single newline
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
        for file in files if file.endswith(".feature")
    ]

    if not feature_files:
        print("⚠️ No .feature files found to process.")
        return

    for file in feature_files:
        fix_gherkin_indentation(file)

    print("✅ Gherkin indentation fixed successfully! No extra blank lines!")


if __name__ == "__main__":
    feature_files_dir = get_feature_files_directory()
    process_feature_files(feature_files_dir)
