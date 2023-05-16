"""
video_extension_changer.py

This script changes the extensions of video files in a specified directory and its subdirectories to '.mp4'.
It supports various video file extensions, including AVI, WMV, FLV, MOV, MPG, MPEG, M4V, 3GP, and ASX.

Usage:
    python video_extension_changer.py <dir_path>

Arguments:
    dir_path (str): Directory path containing the video files.

Dependencies:
    - os
    - sys

Author: K H M BURHAN UDDIN
Date: May 12, 2023
Version: 1.0
"""

import os
import sys

VIDEO_EXTENSIONS = ['.avi', '.wmv', '.flv', '.mov', '.mpg', '.mpeg', '.m4v', '.3gp', '.asx']


def change_video_extensions(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(file_path)[1]
            if file_ext.lower() in VIDEO_EXTENSIONS:
                new_file_path = os.path.splitext(file_path)[0] + '.mp4'
                os.rename(file_path, new_file_path)
                print(f"Renamed {file_path} to {new_file_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <dir_path>")
        sys.exit(1)
    dir_path = sys.argv[1]
    change_video_extensions(dir_path)
