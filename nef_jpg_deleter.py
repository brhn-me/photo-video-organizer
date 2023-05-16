"""
nef_jpg_deleter.py

This script deletes Nikon Electronic Format (NEF) raw image files if a corresponding JPEG file with the same name exists
in a specified source folder and its subfolders. The script searches for NEF files and checks if a corresponding JPEG file
exists by replacing the extension with '.jpg'.

Usage:
    python3 nef_jpg_deleter.py <source_folder>

Arguments:
    source_folder (str): Path to the source folder.

Dependencies:
    - os
    - sys

Author: K H M BURHAN UDDIN
Date: May 12, 2023 
Version: 1.0
"""

import os
import sys

def delete_nef_with_jpg(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.nef'):
                jpg_file = os.path.splitext(file)[0] + '.jpg'
                jpg_path = os.path.join(root, jpg_file)
                nef_path = os.path.join(root, file)
                if os.path.exists(jpg_path):
                    os.remove(nef_path)
                    print(f"Deleted {nef_path}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 resizer.py <source_folder>")
        sys.exit(1)
    source_folder = sys.argv[1]
    delete_nef_with_jpg(source_folder)
