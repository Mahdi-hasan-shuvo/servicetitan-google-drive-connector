
# main.py
# Author: Mahdi Hasan Shuvo
# Developer: Mahdi Hasan Shuvo
# Version: 1.0
# ---- Imports Libraries ----

from servicetitan import API as webAPI
from Google.api import GoogleDriveManager  # Import the class directly
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import time
import ssl
from mahdix import *
loeads_data = json.load(open('config.json'))
coki = loeads_data['Cookies']
print_lock = Lock()

def uploads_and_downloads(sourceId, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Create a NEW API instance for each thread
            drive_api = GoogleDriveManager()  # Now this works!
            
            # with print_lock:
                # print(f"Syncing files...{LI_WHITE}Source ID: {LI_BLUE}{sourceId}{LI_WHITE}")
            
            folder = webAPI.get_all_folder_id(sourceId=sourceId, coki=coki)
            d_folder = drive_api.get_all_folders()
            
            with print_lock:
                print(f"[{len(d_folder)}] Syncing files...{LI_WHITE}Source ID: {LI_BLUE}{sourceId}{LI_WHITE}")
                # print(f'[{len(d_folder)}] Folders found on Drive')
            
            for d in d_folder:
                for f in folder:
                    if d['name'].lower() == f['name'].lower():
                        get_all_file_web = webAPI.get_file_info(sourceId, f['id'], coki)
                        get_all_file_drive = drive_api.get_files_in_folder(d['id'])
                        
                        web_files = {file['name']: file['id'] for file in get_all_file_web}
                        drive_files = {file['name']: file['id'] for file in get_all_file_drive}
                        
                        # Web → Drive missing
                        for name, file_id in web_files.items():
                            if name not in drive_files:
                                with print_lock:
                                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {LI_WHITE}Name: {LI_CYAN}{name} {LI_YELLOW}| {LI_WHITE}ID: {LI_BLUE}{file_id}{LI_WHITE}")
                                downloads_path = webAPI.DownloadFile(
                                    url=f'https://go.servicetitan.com/app/api/fam/documents/files/{file_id}/content?toOpen=true',
                                    output_file=name,
                                    coki=coki
                                )
                                drive_api.upload_file(folder_id=d['id'], local_file_path=downloads_path)
                                os.remove(downloads_path)
                        
                        # Drive → Web missing
                        for name, file_id in drive_files.items():
                            if name not in web_files:
                                with print_lock:
                                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {LI_WHITE}Name: {LI_CYAN}{name} {LI_YELLOW}| {LI_WHITE}ID: {LI_BLUE}{file_id}{LI_WHITE}")
                                d_path = drive_api.download_file(file_id=file_id, destination_path='Downloads')
                                webAPI.Uploads_file(file_path=d_path, sourceId=sourceId, folder_id=f['id'], coki=coki)
                                os.remove(d_path)
            
            return True  # Success
            
        except ssl.SSLError as e:
            with print_lock:
                print(f"SSL Error for {sourceId} (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)
            
        except Exception as e:
            with print_lock:
                print(f"Error for {sourceId} (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(2 ** attempt)
    
    return False
while True:
    get_uis = webAPI.serch_project_id(coki=coki)
    
    # Use only 2 workers to avoid SSL overload
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(uploads_and_downloads, sid): sid for sid in get_uis}
        
        for future in as_completed(futures):
            sid = futures[future]
            try:
                result = future.result()
                if not result:
                    print(f"Failed to process {sid} after all retries")
            except Exception as e:
                print(f"Unexpected error for {sid}: {e}")
    
    print(f'[{datetime.now().strftime("%H:%M:%S")}] Cycle complete. Waiting...')
    time.sleep(10)








