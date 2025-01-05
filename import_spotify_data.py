from datetime import datetime
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from kozubenko.os import Downloads_Directory
from definitions import TEMP_DIR, SPOTIFY_USER_DATA_DIR, SPOTIFY_ACCOUNT_DATA, SPOTIFY_EXTENDED_STREAMING_HISTORY, SPOTIFY_TECHNICAL_LOG, SPOTIFY_ARCHIVED_USER_DATA_DIR

from zipfile import ZipFile, ZIP_DEFLATED


def save_user_data_to_project_files(name:str, path_to_zip: str):
    print(f'path_to_zip: {path_to_zip}')
    given_zip = ZipFile(path_to_zip)
    for file_name in given_zip.namelist():
        if file_name == SPOTIFY_ACCOUNT_DATA + '/':
            zipped_account_data = os.path.join(path_to_zip, SPOTIFY_ACCOUNT_DATA)
            destination_dir = os.path.join(SPOTIFY_USER_DATA_DIR, name, SPOTIFY_ACCOUNT_DATA)
            
            

        
        if file_name == SPOTIFY_EXTENDED_STREAMING_HISTORY + '/':
            zipped_account_data = os.path.join(path_to_zip, SPOTIFY_EXTENDED_STREAMING_HISTORY)
            destination_dir = os.path.join(SPOTIFY_USER_DATA_DIR, name, SPOTIFY_EXTENDED_STREAMING_HISTORY)

            if os.path.exists(destination_dir):     # Save old data under: 'Spotify User Data\archive', as: 'Spotify Extended Streaming History - 2025-01-01'
                created_at = datetime.fromtimestamp(os.path.getctime(destination_dir)).strftime('%Y-%m-%d')
                archived_folder_target_dir = os.path.join(SPOTIFY_ARCHIVED_USER_DATA_DIR, name)
                Path(archived_folder_target_dir).mkdir(parents=True, exist_ok=True)

                archived_folder_name = f'{SPOTIFY_EXTENDED_STREAMING_HISTORY} - {created_at}.zip'
                archived_folder_target_dir = os.path.join(archived_folder_target_dir, archived_folder_name)
                
                with ZipFile(archived_folder_target_dir, 'w', ZIP_DEFLATED) as zip_ref:
                    for root, folder_names, file_names in os.walk(destination_dir):
                        for file_name in file_names:
                            if file_name.endswith('.json'):     # Only want to save the json files holding the data. Goal: avoid the pdf readfirst files.
                                name = os.path.join(root, file_name)
                                arc_name = os.path.relpath(name, os.path.join(destination_dir, '..'))
                                zip_ref.write(name, arc_name)

        if file_name == SPOTIFY_TECHNICAL_LOG + '/':
            temp_dir = os.path.join(TEMP_DIR, 'Spotify Technical Log Information')

    given_zip.close()



# name = input('What name should we save this file under?: ')

# root = tk.Tk()
# root.attributes('-topmost',True, '-alpha',0)

# path_to_zip = filedialog.askopenfilename(initialdir=Downloads_Directory(), title='Select my_spotify_data*.zip', filetypes=[('zip files', '*.zip')])

name = 'Stan' 
path_to_zip = 'C:/Users/stasp/Downloads/my_spotify_data.zip'

save_user_data_to_project_files(name, path_to_zip)

# print(f'{name}: {path_to_zip}')



