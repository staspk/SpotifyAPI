"""
`py ./import_Spotify_Data.py {name}`
    `{name}:str` -> owner of the Spotify Data. Separate `*.zips` will be categorized under this name. See: `SpotifyUser`

Spotify Data Types:
    - Spotify Account Data
    - Spotify Extended Streaming History
    - Spotify Technical Log Information
"""
import os, argparse
from typing import Optional
from tkinter import Tk, filedialog
from zipfile import ZIP_LZMA, ZipFile
from kozubenko.datetime import local_time_as_legal_filename
from kozubenko.print import Print
from kozubenko.os import Directory, Downloads_Directory, File
from Spotify_Data_Types import USER_DATA_DIR, Spotify_Data_Type



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', help='owner of the Spotify Data. Separate `*.zips` [Spotify Data Types] will be categorized under this name.')
    args = parser.parse_args()

    if not args.name:
        Print.red('import_Spotify_Data.py: name {arg1} is required. For details, run: `py import_Spotify_Data.py --help`')
        exit(0)


class Test:
    def archive_has_correctly_zipped_all_old_files(data_directory:Directory, archive_dest:Directory) -> bool:
        original_file_names:set[str] = set()

        for file in data_directory.files():
            original_file_names.add(file.name)

        for file in ZipFile(archive_dest, 'r').namelist():
            if not File(file).name in original_file_names:
                return False

        return True

def archive(name:str, data_type:Spotify_Data_Type) -> Directory:
    """
    Caller should check if `archive()` necessary. Will throw if `data_to_archive` is empty!

    **Returns:**
        - If zipped folder absolute path 
    """
    data_to_archive = USER_DATA_DIR(name, data_type)
    DESTINATION = Directory(USER_DATA_DIR(name), 'ARCHIVE', data_type, f'{local_time_as_legal_filename()}.zip')

    if not data_to_archive.empty():
        with ZipFile(DESTINATION.ensure_parents(), 'w', compression=ZIP_LZMA) as zip:
            for file in data_to_archive.files():
                zip.write(file, os.path.relpath(file, file.parent.parent))

        return DESTINATION
    
    return Exception(f'archive(name={name}, data_type={data_type}): archive() called on an empty Directory')

def identify_Spotify_Data_Type(zip:ZipFile) -> Spotify_Data_Type | Exception:
    """
    Identified by the root folder in 'my_spotify_data.zip'
        name of root folder == `Spotify_Data_Type`

    Remarks:
    --------
    **`zip.namelist()` Returns:**
        Spotify Extended Streaming History/Streaming_History_Audio_2016-2018_0.json
        ...
        Spotify Extended Streaming History/Streaming_History_Video_2018-2026.json
        Spotify Extended Streaming History/
        Spotify Extended Streaming History/ReadMeFirst_ExtendedStreamingHistory.pdf

    `containing_folder` -> "Spotify Extended Streaming History"
    """
    root_folder_name = zip.namelist()[0].split('/', maxsplit=1)[0]

    if root_folder_name in Spotify_Data_Type:
        return Spotify_Data_Type(root_folder_name)
    
    raise Exception('identify_Spotify_Data_Type(): Given .zip does not contain a standard Spotify_Data_Type!')

def Import_Spotify_Data(name:str, path_to_zip:Optional[str]=None) -> None | Exception:
    """
    Unzips only jsons from 'my_spotify_data.zip' to avoid extraneous files, e.g. readme.pdf

    **Parameters**:
        - `name` - data owner/username. Becomes name of the folder under which data is stored.
        - `path_to_zip` - path to 'my_spotify_data.zip'. If not provided, filedialog opens for user to manually select .zip.
    """
    if path_to_zip is None:
        root = Tk()
        root.attributes('-topmost',True, '-alpha',0)
        path_to_zip = filedialog.askopenfilename(initialdir=Downloads_Directory(), title='Select my_spotify_data*.zip', filetypes=[('zip files', '*.zip')])

    zip = ZipFile(path_to_zip, 'r')
    data_type = identify_Spotify_Data_Type(zip)
    data_dest = Directory(USER_DATA_DIR(name), data_type)   # i.e: ./Spotify User Data/{name}/{Spotify_Data_Type}

    if data_dest.exists() and not data_dest.empty():
        archive_dest:Directory = archive(name, data_type)
        if not Test.archive_has_correctly_zipped_all_old_files(data_dest, archive_dest):
            raise Exception('Import_Spotify_Data(): Cannot Proceed, TEST FAILED!')
        archive_dest.delete()
    else:
        archive_dest = None

    for file in zip.namelist():   # e.g: "Spotify Extended Streaming History/Streaming_History_Audio_2016-2018_0.json"
        if file.endswith('.json'):
            zip.extract(file, data_dest.parent)   # root_folder in my_spotify_data.zip IS destination, thus destination.parent passed in as alternate `path` 

    zip.close()

    Print.green(f'Import_Spotify_Data(name={name}, path_to_zip={path_to_zip}): SUCCESS!')
    Print.green(f'   data_type = {data_type}')
    Print.green(f'   data_dest = {data_dest}')
    if archive_dest:
        Print.green(f'   old data archived to = {archive_dest}')



if __name__ == "__main__":
    Import_Spotify_Data(args.name)




