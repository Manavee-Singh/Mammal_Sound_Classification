import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Set the credentials file path
credentials_file = 'your-credentials-file.json'  # Replace with your credentials file

# Set the folder ID of the Google Drive folder you want to list files from
folder_id = 'your-folder-id'  # Replace with your folder ID

# Create a service object
creds = service_account.Credentials.from_service_account_file(credentials_file)
drive_service = build('drive', 'v3', credentials=creds)

# Function to list all files in a folder
def list_files_in_folder(folder_id):
    results = drive_service.files().list(q=f"'{folder_id}' in parents and trashed = false", fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

# Get the list of files in the folder
files_in_folder = list_files_in_folder(folder_id)

# Print the file names
for file in files_in_folder:
    print(f"File Name: {file['name']}")

