import os
import re

def get_feature_files_directory():
    """Automatically detect the project's feature files directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    feature_files_dir = os.path.join(project_root, "features")

    if not os.path.exists(feature_files_dir):
        print(f"⚠️ Warning: Feature files directory '{feature_files_dir}' not found.")
    return feature_files_dir


def fix_gherkin_indentation(file_path):
    """Fix indentation for And/But statements within Scenarios using 2 spaces."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    formatted_lines = []
    inside_scenario = False

    for line in lines:
        stripped = line.lstrip()

        # Detect the start of a scenario, examples, rule, or feature
        if stripped.startswith(("Scenario", "Examples", "Rule", "Feature")):
            inside_scenario = True
            formatted_lines.append(line)
            continue

        # Properly indent And/But within scenarios (2 spaces instead of 4)
        if stripped.startswith(("And", "But")) and inside_scenario:
            formatted_lines.append("  " + stripped)  # Use 2 spaces instead of 4
        else:
            formatted_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(formatted_lines)


def process_feature_files(directory):
    """Process all .feature files and fix indentation."""
    if not os.path.exists(directory):
        print("🚨 Feature files directory not found! Check your project structure.")
        return

    feature_files = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if file.endswith(".feature")]

    if not feature_files:
        print("⚠️ No .feature files found to process.")
        return

    for file in feature_files:
        fix_gherkin_indentation(file)

    print("✅ Gherkin indentation fixed successfully for all feature files (2 spaces)!")


if __name__ == "__main__":
    feature_files_dir = get_feature_files_directory()
    process_feature_files(feature_files_dir)
