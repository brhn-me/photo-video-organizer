"""
converted_video_organizer.py

This script organizes converted video files in a specified directory and its subdirectories. It checks for converted videos
that have a corresponding original video file and performs the following actions:

1. Checks if the converted file size is larger than the original file size. If it is, the converted file is removed.
2. Sets the modified and created date of the converted file to that of the original file.
3. Deletes the original file and renames the converted file to the original filename with mp4 as file extension.

Usage:
    python converted_video_organizer.py <dir_path>

Arguments:
    dir_path (str): Path to the directory containing the converted video files.

Dependencies:
    - os
    - sys

Author: K H M BURHAN UDDIN
Date: May 12, 2023
Version: 1.0
"""

import os
import sys


def get_converted_filename(original_filename):
    base, ext = os.path.splitext(original_filename)
    return f"{base}-converted.mp4"


def organize_converted_videos(dir_path):
    file_pairs = []
    total_original_size = 0
    total_converted_size = 0
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            original_path = os.path.join(root, filename)
            if os.path.isfile(original_path) and not filename.endswith("-converted.mp4"):
                converted_filename = get_converted_filename(filename)
                converted_path = os.path.join(root, converted_filename)
                if os.path.isfile(converted_path):
                    original_size = os.path.getsize(original_path)
                    converted_size = os.path.getsize(converted_path)

                    if converted_size > original_size:
                        print(f"Error: Converted file {converted_path} is larger than original file {original_path}. Removing converted file.")
                        os.remove(converted_path)
                    else:
                         # set modified and created date of converted file to that of original file
                        original_stat = os.stat(original_path)
                        os.utime(converted_path, (original_stat.st_atime, original_stat.st_mtime))
                        print(f"Converted file {converted_path} modified and created date updated to that of original file {original_path}")

                        # Delete original file and rename converted file to original filename
                        os.remove(original_path)
                        new_path = os.path.splitext(original_path)[0] + ".mp4"
                        os.rename(converted_path, new_path)
                        print(f"Deleted {original_path} and renamed {converted_path} to {new_path}")

                        file_pairs.append((original_path, converted_path, original_size, converted_size))

    for original_path, converted_path, original_size, converted_size in file_pairs:
        total_original_size += original_size
        total_converted_size += converted_size
        print(f"{original_path} ({human_readable_size(original_size)} -> {human_readable_size(converted_size)})")

    print(f"Total Size: {human_readable_size(total_original_size)}")
    print(f"Converted Size: {human_readable_size(total_converted_size)}")
    print(f"Saved: {human_readable_size(total_original_size - total_converted_size)}")
    


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <dir_path>")
        sys.exit(1)
    dir_path = sys.argv[1]
    organize_converted_videos(dir_path)
