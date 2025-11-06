"""
`py ./import_spotify_data.py {name}`
    `{name}:str` -> owner of the Spotify Data. Separate `*.zips` will be categorized under this name. See: `SpotifyUser`

Spotify Data Types:
    - Spotify Account Data
    - Spotify Extended Streaming History
    - Spotify Technical Log Information

"""
import os, argparse, shutil
from datetime import datetime
from pathlib import Path
from tkinter import Tk, filedialog

from kozubenko.os import Downloads_Directory
from definitions import SPOTIFY_USER_DATA_DIR, SPOTIFY_USER_DATA_ARCHIVE_DIR
from definitions import SPOTIFY_ACCOUNT_DATA, SPOTIFY_EXTENDED_STREAMING_HISTORY, SPOTIFY_TECHNICAL_LOG

from zipfile import ZipFile, ZIP_DEFLATED

from kozubenko.print import Print


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', help='owner of the Spotify Data. Separate `*.zips` [Spotify Data Types] will be categorized under this name.')
    args = parser.parse_args()

    if not args.name:
        Print.red('import_spotify_data.py: name {arg1} is required. For details, run: `py import_spotify_data.py --help`')
        exit(0)


# dir_to_archive => full path of directory to archive; DATA_CATEGORY => See 'my_spotify_data.zip' Folder Names in definitions.py
def archive(dir_to_archive:str, DATA_CATEGORY):
    created_at = datetime.fromtimestamp(os.path.getctime(dir_to_archive)).strftime('%Y-%m-%d')
    name = dir_to_archive.split('\\')[-2]
    output_target_dir = os.path.join(SPOTIFY_USER_DATA_ARCHIVE_DIR, name)
    Path(output_target_dir).mkdir(parents=True, exist_ok=True)

    data_category = dir_to_archive.split('\\')[-1]
    # print(f'Data Category: {data_category}')
    output_folder_name = f'{data_category} - {created_at}.zip'                  # example: 'Spotify Extended Streaming History - 2025-01-01'
    output_target_dir = os.path.join(output_target_dir, output_folder_name)
    
    with ZipFile(output_target_dir, 'w', ZIP_DEFLATED) as zip_ref:
        for cur_dir, folder_names, file_names in os.walk(dir_to_archive):
            for file_name in file_names:
                file = os.path.join(cur_dir, file_name)
                arc_name = os.path.relpath(file, os.path.join(dir_to_archive, '..'))
                zip_ref.write(file, arc_name)
    
    shutil.rmtree(dir_to_archive, ignore_errors=False)      # Deleting folder    
    print(f'Archive(): dir_to_archive: {dir_to_archive}')


def handle_unzip(zipfile_ref:ZipFile, target_folder_in_zip:str, dest_dir:str):
    if os.path.exists(dest_dir):
        archive(dest_dir, target_folder_in_zip)
    
    for file_name in zipfile_ref.namelist():
        if file_name.startswith(target_folder_in_zip + '/') and file_name.endswith('.json'):   # Only .jsons to avoid importing extraneous files, e.g. readme.pdf
            zipfile_ref.extract(file_name, os.path.join(dest_dir, '..'))
    print(f'handle_unzip(): target_folder_in_zip: {target_folder_in_zip}, dest_dir: {dest_dir}')

def save_user_data_to_project_files(name:str, path_to_zip: str):
    """
    name: data owner/username. Becomes name of the folder under which data is stored.\n
    path_to_zip: path to 'my_spotify_data.zip'
    """
    given_zip = ZipFile(path_to_zip, 'r')
    for file_name in given_zip.namelist():
        if file_name == SPOTIFY_ACCOUNT_DATA + '/':
            handle_unzip(given_zip, SPOTIFY_ACCOUNT_DATA, os.path.join(SPOTIFY_USER_DATA_DIR, name, SPOTIFY_ACCOUNT_DATA))

        if file_name == SPOTIFY_EXTENDED_STREAMING_HISTORY + '/':
            handle_unzip(given_zip, SPOTIFY_EXTENDED_STREAMING_HISTORY, os.path.join(SPOTIFY_USER_DATA_DIR, name, SPOTIFY_EXTENDED_STREAMING_HISTORY))
            
        if file_name == SPOTIFY_TECHNICAL_LOG + '/':
            handle_unzip(given_zip, SPOTIFY_TECHNICAL_LOG, os.path.join(SPOTIFY_USER_DATA_DIR, name, SPOTIFY_TECHNICAL_LOG))

    given_zip.close()

def Import_Spotify_Data(name:str):
    root = Tk()
    root.attributes('-topmost',True, '-alpha',0)

    path_to_zip = filedialog.askopenfilename(initialdir=Downloads_Directory(), title='Select my_spotify_data*.zip', filetypes=[('zip files', '*.zip')])

    save_user_data_to_project_files(name, path_to_zip)


if __name__ == "__main__":
    Import_Spotify_Data(args.name)