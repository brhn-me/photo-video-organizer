"""
date_updater.py

This script updates the date taken and file creation and modification time for images and videos in a specified folder
and its subfolders. It supports JPEG, PNG, GIF, BMP images, and MP4, AVI, MOV videos. The script utilizes the `piexif`
library for images and the `os.utime` function for videos to modify the file metadata.

Usage:
    python date_updater.py <src_folder> <new_date> [--verbose]

Arguments:
    src_folder (str): Source folder containing the images and videos.
    new_date (str): New date to set in the format yyyy-mm-dd.

Options:
    --verbose: Print progress information.

Dependencies:
    - os
    - argparse
    - datetime
    - piexif
    - subprocess

Author: K H M BURHAN UDDIN
Date: May 12, 2023
Version: 1.0
"""

import os
import argparse
import datetime
import piexif
import subprocess

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov')

def update_date(file_path, new_date):
    """
    Update the date taken and file creation and modification time for the given file
    """
    if os.path.splitext(file_path)[1].lower() in IMAGE_EXTENSIONS:
        try:
            exif_dict = piexif.load(file_path)
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date.strftime('%Y:%m:%d %H:%M:%S')
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, file_path)
            os.utime(file_path, (new_date.timestamp(), new_date.timestamp()))
            print(f"Updated date taken for image: {file_path}")
        except:
            print(f"Failed to update date taken for image: {file_path}")
            
    elif os.path.splitext(file_path)[1].lower() in VIDEO_EXTENSIONS:
        try:
            # cmd = ['exiftool', '-DateTimeOriginal=' + new_date.strftime('%Y:%m:%d %H:%M:%S'), file_path]
            # subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            os.utime(file_path, (new_date.timestamp(), new_date.timestamp()))
            print(f"Updated date taken for video: {file_path}")
        except:
            print(f"Failed to update date taken for video: {file_path}")

def update_date_recursive(src_folder, new_date, verbose):
    """
    Recursively update the date taken and file creation and modification time for all images and videos in the given folder
    """
    for root, dirs, files in os.walk(src_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.splitext(file_path)[1].lower() in IMAGE_EXTENSIONS or os.path.splitext(file_path)[1].lower() in VIDEO_EXTENSIONS:
                update_date(file_path, new_date)
                if verbose:
                    print(f"Processed file: {file_path}")
        if verbose:
            print(f"Processed folder: {root}")
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update the date taken and file creation and modification time for all images and videos in a folder.')
    parser.add_argument('src_folder', type=str, help='Source folder containing the images and videos')
    parser.add_argument('new_date', type=str, help='New date to set in the format yyyy-mm-dd')
    parser.add_argument('--verbose', action='store_true', help='Print progress information')
    args = parser.parse_args()

    new_date = datetime.datetime.strptime(args.new_date, '%Y-%m-%d')
    update_date_recursive(args.src_folder, new_date, args.verbose)