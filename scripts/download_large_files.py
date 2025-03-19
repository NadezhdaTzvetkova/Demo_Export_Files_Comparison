import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Load credentials securely from an environment variable
CREDENTIALS_PATH = os.getenv("GDRIVE_CREDENTIALS", "~/gdrive_credentials.json")
FOLDER_NAME = "Bank Export Files"  # Update with your Google Drive folder name
DOWNLOAD_DIR = "test_data/"  # Local folder for downloaded files


def authenticate_drive():
    """Authenticate Google Drive API using service account."""
    creds = service_account.Credentials.from_service_account_file(
        os.path.expanduser(CREDENTIALS_PATH)
    )
    return build("drive", "v3", credentials=creds)


def find_folder_id(service, folder_name):
    """Retrieve the Google Drive folder ID by name."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if not folders:
        print(f"⚠️ Folder '{folder_name}' not found in Google Drive.")
        return None

    return folders[0]["id"]


def list_files(service, folder_id):
    """List all files in the given Google Drive folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get("files", [])


def download_file(service, file_id, file_name):
    """Download a file from Google Drive if it doesn't already exist locally."""
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if os.path.exists(file_path):
        print(f"✅ {file_name} already exists. Skipping download.")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    request = service.files().get_media(fileId=file_id)

    with open(file_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(
                f"📥 Downloading {file_name}: {int(status.progress() * 100)}% complete"
            )


def main():
    """Authenticate, find the folder, list files, and download them in bulk."""
    print("🚀 Starting bulk download from Google Drive...")
    service = authenticate_drive()
    folder_id = find_folder_id(service, FOLDER_NAME)

    if not folder_id:
        print("❌ No valid folder found. Exiting.")
        return

    files = list_files(service, folder_id)

    if not files:
        print("⚠️ No files found in the specified folder.")
        return

    for file in files:
        print(f"➡️ Processing: {file['name']}")
        download_file(service, file["id"], file["name"])

    print("🎉 All files have been downloaded successfully!")


if __name__ == "__main__":
    main()
