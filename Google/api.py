"""
Google Drive Manager - Complete Python Script
Features:
✅ Get all folders from Google Drive
✅ List files inside each folder
✅ Download files from Drive → your PC
✅ Upload files from PC → Drive folder
"""

import json
import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import json
loeads_data = json.load(open('config.json'))
# Define the scopes - full access to Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]

class GoogleDriveManager:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Drive API (Correct way)"""
        creds = None

        TOKEN_FILE = loeads_data['TOKEN_FILE']#"Joot998@gmail.com_tokenf_.json"
        CLIENT_SECRET_FILE =loeads_data['CLIENT_SECRET_FILE'] #r"client_secret.json"
        # ☝️ Put your real OAuth client credentials file path here

        # Load saved token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # If no valid token -> login again
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE,
                    redirect_uri="http://localhost:5000/oauth2callback",
                    scopes=SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save token for future
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)
    
    # ============================================================
    # ✅ 1. GET ALL FOLDERS FROM GOOGLE DRIVE
    # ============================================================
    def get_all_folders(self):
        """Get all folders from Google Drive"""
        folders = []
        page_token = None
        
        while True:
            results = self.service.files().list(
                q="mimeType='application/vnd.google-apps.folder' and trashed=false",
                spaces='drive',
                # fields='nextPageToken, files(id, name, parents)',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token,
                pageSize=100
            ).execute()
            
            folders.extend(results.get('files', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        return folders
    
    def print_all_folders(self):
        """Print all folders with their IDs"""
        folders = self.get_all_folders()
        print(f"\n📁 Found {len(folders)} folders:\n")
        print("-" * 60)
        for folder in folders:
            print(f"📂 {folder['name']}")
            print(f"   ID: {folder['id']}")
            print("-" * 60)
        return folders
    
    # ============================================================
    # ✅ 2. LIST FILES INSIDE EACH FOLDER
    # ============================================================
    def get_files_in_folder(self, folder_id):
        """Get all files inside a specific folder"""
        files = []
        page_token = None
        
        while True:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, size, createdTime)',
                pageToken=page_token,
                pageSize=100
            ).execute()
            
            files.extend(results.get('files', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        return files
    
    def list_all_folders_with_files(self):
        """List all folders and their contents"""
        folders = self.get_all_folders()
        
        print(f"\n📊 Complete Drive Structure ({len(folders)} folders):\n")
        print("=" * 70)
        
        for folder in folders:
            print(f"\n📂 FOLDER: {folder['name']}")
            print(f"   Folder ID: {folder['id']}")
            
            files = self.get_files_in_folder(folder['id'])
            
            if files:
                print(f"   📄 Files ({len(files)}):")
                for file in files:
                    size = file.get('size', 'N/A')
                    if size != 'N/A':
                        size = f"{int(size) / 1024:.2f} KB"
                    print(f"      • {file['name']} ({size})")
            else:
                print("   📄 (Empty folder)")
            
            print("-" * 70)
        
        return folders
    
    # ============================================================
    # ✅ 3. DOWNLOAD FILES FROM DRIVE → YOUR PC
    # ============================================================
    def download_file(self, file_id, destination_path):
        """Download a single file from Google Drive"""
        # Get file metadata
        file_metadata = self.service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name', 'downloaded_file')
        
        # Full path for saving
        full_path = os.path.join(destination_path, file_name)
        
        # Create destination directory if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)
        
        # Download the file
        request = self.service.files().get_media(fileId=file_id)
        
        with io.FileIO(full_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                # print(f"⬇️  Downloading {file_name}: {int(status.progress() * 100)}%")
        
        print(f"✅ Downloaded: {full_path}")
        return full_path
    
    def download_folder(self, folder_id, destination_path):
        """Download all files from a folder"""
        # Get folder name
        folder_metadata = self.service.files().get(fileId=folder_id).execute()
        folder_name = folder_metadata.get('name', 'downloaded_folder')
        
        # Create local folder
        local_folder = os.path.join(destination_path, folder_name)
        os.makedirs(local_folder, exist_ok=True)
        
        # Get all files in the folder
        files = self.get_files_in_folder(folder_id)
        
        print(f"\n📥 Downloading folder: {folder_name} ({len(files)} files)")
        print("-" * 50)
        
        downloaded_files = []
        for file in files:
            # Skip Google Docs/Sheets/Slides (they need export)
            if 'google-apps' in file.get('mimeType', ''):
                print(f"⏭️  Skipping Google Doc: {file['name']}")
                continue
            
            try:
                path = self.download_file(file['id'], local_folder)
                downloaded_files.append(path)
            except Exception as e:
                print(f"❌ Error downloading {file['name']}: {e}")
        
        print(f"\n✅ Downloaded {len(downloaded_files)} files to: {local_folder}")
        return downloaded_files
    
    def download_all_drive(self, destination_path='./drive_backup'):
        """Download entire Google Drive"""
        folders = self.get_all_folders()
        
        print(f"\n🚀 Starting full Drive backup to: {destination_path}")
        
        # Download root files (files not in any folder)
        root_files = self.service.files().list(
            q="'root' in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'",
            fields='files(id, name, mimeType)'
        ).execute().get('files', [])
        
        if root_files:
            print(f"\n📁 Downloading root files ({len(root_files)} files)")
            for file in root_files:
                if 'google-apps' not in file.get('mimeType', ''):
                    try:
                        self.download_file(file['id'], destination_path)
                    except Exception as e:
                        print(f"❌ Error: {e}")
        
        # Download each folder
        for folder in folders:
            try:
                self.download_folder(folder['id'], destination_path)
            except Exception as e:
                print(f"❌ Error downloading folder {folder['name']}: {e}")
        
        print(f"\n🎉 Backup complete! Saved to: {destination_path}")
    
    # ============================================================
    # ✅ 4. UPLOAD FILES FROM PC → DRIVE FOLDER
    # ============================================================
    def upload_file(self, local_file_path, folder_id=None):
        """Upload a single file to Google Drive"""
        file_name = os.path.basename(local_file_path)
        
        # File metadata
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Upload the file
        media = MediaFileUpload(local_file_path, resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"✅ Uploaded: {file_name}")
        # print(f"   File ID: {file.get('id')}")
        # print(f"   Link: {file.get('webViewLink')}")
        
        return file
    
    def upload_folder(self, local_folder_path, parent_folder_id=None):
        """Upload an entire local folder to Google Drive"""
        folder_name = os.path.basename(local_folder_path)
        
        # Create folder in Drive
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        
        drive_folder = self.service.files().create(
            body=folder_metadata,
            fields='id, name'
        ).execute()
        
        drive_folder_id = drive_folder.get('id')
        print(f"\n📂 Created folder: {folder_name} (ID: {drive_folder_id})")
        
        # Upload all files in the folder
        uploaded_files = []
        for item in os.listdir(local_folder_path):
            item_path = os.path.join(local_folder_path, item)
            
            if os.path.isfile(item_path):
                try:
                    file = self.upload_file(item_path, drive_folder_id)
                    uploaded_files.append(file)
                except Exception as e:
                    print(f"❌ Error uploading {item}: {e}")
            elif os.path.isdir(item_path):
                # Recursively upload subfolders
                self.upload_folder(item_path, drive_folder_id)
        
        print(f"✅ Uploaded {len(uploaded_files)} files to folder: {folder_name}")
        return drive_folder
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """Create a new folder in Google Drive"""
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
        
        folder = self.service.files().create(
            body=folder_metadata,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"✅ Created folder: {folder_name}")
        print(f"   Folder ID: {folder.get('id')}")
        
        return folder
    
    # ============================================================
    # BONUS: SEARCH FILES
    # ============================================================
    def search_files(self, query_name):
        """Search for files by name"""
        results = self.service.files().list(
            q=f"name contains '{query_name}' and trashed=false",
            spaces='drive',
            fields='files(id, name, mimeType, parents)',
            pageSize=50
        ).execute()
        
        files = results.get('files', [])
        print(f"\n🔍 Search results for '{query_name}': {len(files)} files")
        for file in files:
            print(f"   • {file['name']} (ID: {file['id']})")
        
        return files
