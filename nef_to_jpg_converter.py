"""
nef_to_jpg_converter.py

This script converts Nikon Electronic Format (NEF) raw image files to JPEG format in a specified source folder
and its subfolders. It utilizes the 'convert' command-line tool from the ImageMagick software to perform the conversion.

Usage:
    python nef_to_jpg_converter.py <source_folder>

Arguments:
    source_folder (str): Path to the source folder containing the NEF files.

Dependencies:
    - argparse
    - os
    - subprocess

Author: K H M BURHAN UDDIN
Date: May 12, 2023 
Version: 1.0
"""

import argparse
import os
import subprocess

def convert_nef_to_jpg(source_folder):
    for root, _, files in os.walk(source_folder):
        for filename in files:
            if filename.lower().endswith('.nef'):
                nef_path = os.path.join(root, filename)
                jpg_path = os.path.splitext(nef_path)[0] + '.jpg'
                subprocess.run(['convert', nef_path, jpg_path])
                os.remove(nef_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder', help='Path to the source folder')
    args = parser.parse_args()
    convert_nef_to_jpg(args.source_folder)
