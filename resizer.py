"""
resizer.py

This script resizes images in a specified folder and its subfolders to 4K resolution (3840x2160) if they exceed this size.
It supports JPEG and PNG image formats. The script utilizes the `PIL` (Python Imaging Library) module to open and resize images.

Usage:
    python3 resizer.py <source_folder>

Arguments:
    source_folder (str): Source folder containing the images.

Dependencies:
    - PIL (Python Imaging Library)
    - os

Author: K H M BURHAN UDDIN
Date: May 12, 2023    
Version: 1.0
"""

from PIL import Image
import os

def resize_images(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in ['.jpg', '.jpeg', '.png']:
                with Image.open(file_path) as img:
                    if img.width > 3840 or img.height > 2160:
                        img.thumbnail((3840, 2160), resample=Image.LANCZOS)
                        img.save(file_path, optimize=True, quality='keep', exif=img.info['exif'])
                        print(f"Resized {file_path} to 4K resolution")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 resizer.py <source_folder>")
        sys.exit(1)
    source_folder = sys.argv[1]
    resize_images(source_folder)
