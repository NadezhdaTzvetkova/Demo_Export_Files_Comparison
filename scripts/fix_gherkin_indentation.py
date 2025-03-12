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
    """Fix indentation for Feature (base), Scenario (base), Given/When/Then (1 tab), And/But (2 tabs)."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    inside_scenario = False
    previous_was_blank = False  # Track blank lines to remove unnecessary ones

    for line in lines:
        stripped = line.strip()

        # Remove excessive blank lines but allow single blank lines between sections
        if stripped == "":
            if previous_was_blank:
                continue  # Skip consecutive blank lines
            previous_was_blank = True
            formatted_lines.append("")  # Keep a single blank line
            continue
        else:
            previous_was_blank = False  # Reset blank line tracker

        # Feature and Scenario remain at base level
        if stripped.startswith(("Feature", "Scenario")):
            formatted_lines.append(stripped)
            inside_scenario = stripped.startswith("Scenario")  # Enable scenario tracking
            continue

        # Given, When, Then → 1 tab
        if stripped.startswith(("Given", "When", "Then")):
            formatted_lines.append("\t" + stripped)

        # And, But → 2 tabs under Given/When/Then
        elif stripped.startswith(("And", "But")):
            formatted_lines.append("\t\t" + stripped)

        # Preserve everything else as is
        else:
            formatted_lines.append(stripped)

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

    print("✅ Gherkin indentation fixed successfully! (1 Tab for Given/When/Then, 2 Tabs for And/But, Blank lines removed)")


if __name__ == "__main__":
    feature_files_dir = get_feature_files_directory()
    process_feature_files(feature_files_dir)
