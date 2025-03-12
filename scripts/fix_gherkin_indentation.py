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
    """Fix indentation for Given/When/Then at base level and And/But indented by 1 Tab."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    inside_scenario = False

    for line in lines:
        stripped = line.lstrip()

        # Detect the start of a Scenario, Examples, Rule, or Feature
        if stripped.startswith(("Scenario", "Examples", "Rule", "Feature")):
            inside_scenario = True
            formatted_lines.append(stripped)  # Keep at base level
            continue

        # Given/When/Then should be at base level (no indentation)
        if stripped.startswith(("Given", "When", "Then")):
            formatted_lines.append(stripped)  # No indentation
        elif stripped.startswith(("And", "But")):
            formatted_lines.append("\t" + stripped)  # Indent And/But by 1 tab
        else:
            formatted_lines.append(stripped)  # Preserve other lines

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines([line + "\n" for line in formatted_lines])  # Ensure newline at end of each line


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

    print("✅ Gherkin indentation fixed successfully! (1 Tab for And/But)")


if __name__ == "__main__":
    feature_files_dir = get_feature_files_directory()
    process_feature_files(feature_files_dir)
