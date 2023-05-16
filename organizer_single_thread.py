"""
organizer_single_thread.py

This script organizes files in a source folder based on their creation date. It creates a destination folder structure
where files are sorted into year and date subdirectories according to their creation date. Files with allowed extensions
are copied to the destination folders, while files with unsupported extensions are copied to an "unorganized" folder.
It tries to set file modified and created date from exif data, if not available it use file meta data.

It does not use multiprocessing or multi threading

Usage:
    python3 organizer_single_thread.py <source_folder>

Dependencies:
    - os
    - shutil
    - exifread
    - datetime
    - sys
    - concurrent.futures

Author: K H M BURHAN UDDIN
Date: May 12, 2023    
Version: 1.0
"""

import os
import shutil
import exifread
from datetime import datetime
import sys

def copy_photos_videos(source_folder):
    parent_dir = os.path.abspath(os.path.join(source_folder, os.pardir))
    destination_folder = os.path.join(parent_dir, f"{os.path.basename(source_folder)}_organized")
    unorganized_folder = os.path.join(parent_dir, f"{os.path.basename(source_folder)}_unorganized")
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.mov', '.3gp', '.nef']
    
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in allowed_extensions:
                try:
                    with open(file_path, 'rb') as f:
                        tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')
                        creation_date = datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
                except (KeyError, TypeError):
                    creation_date = datetime.fromtimestamp(os.path.getctime(file_path))

                destination_folder_path = os.path.join(destination_folder,  creation_date.strftime("%Y"), creation_date.strftime('%Y-%m-%d'))
                os.makedirs(destination_folder_path, exist_ok=True)
                destination_file_path = os.path.join(destination_folder_path, file)
                shutil.copy2(file_path, destination_file_path)
                print(f"Copied {file_path} to {destination_file_path}")
            else:
                unorganized_folder_path = os.path.join(unorganized_folder, os.path.relpath(root, source_folder))
                os.makedirs(unorganized_folder_path, exist_ok=True)
                unorganized_file_path = os.path.join(unorganized_folder_path, file)
                shutil.copy2(file_path, unorganized_file_path)
                print(f"Copied {file_path} to {unorganized_file_path}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 organizer.py <source_folder>")
        sys.exit(1)
    source_folder = sys.argv[1]
    copy_photos_videos(source_folder)
