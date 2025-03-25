import hashlib
import os


def get_file_hash(file_path):
    """Generate MD5 hash for a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_duplicates(root_dir):
    """Find duplicate files in a directory based on file hashes."""
    file_hashes = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                file_hash = get_file_hash(file_path)
                if file_hash in file_hashes:
                    duplicates.append((file_path, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = file_path
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return duplicates


if __name__ == "__main__":
    root_dir = (
        "/Users/Nadezhda.Nikolova/PycharmProjects/" "Demo_Export_Files_Comparison"
    )  # Set this to your project root directory

    duplicates = find_duplicates(root_dir)

    if duplicates:
        for file1, file2 in duplicates:
            print(f"Duplicate found:\n  {file1}\n  {file2}")
    else:
        print("No duplicate files found.")
