import os


def list_created_files_folders(root_dir, level=3):
    # Loop through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude system folders/files (e.g., starting with dot .)
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        filenames[:] = [f for f in filenames if not f.startswith(".")]

        # Calculate the depth of the current directory
        depth = dirpath.count(os.sep) - root_dir.count(os.sep)

        # Skip directories beyond the specified depth
        if depth > level:
            continue

        # Print the directory name
        print(f"Directory: {os.path.basename(dirpath)}")

        # Print files within the directory
        for file in filenames:
            print(f"    File: {file}")


# Replace with the path to your project
project_path = "/Users/Nadezhda.Nikolova/PycharmProjects/Demo_Export_Files_Comparison/"
list_created_files_folders(project_path)
