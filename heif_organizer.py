"""

This script organizes photos in a specified directory and its subdirectories. It checks for JPEG photos that have a
corresponding HEIF photo file and performs the following actions:

1. Checks if the HEIF file size is smaller than the JPEG file size. If it is, the HEIF file is removed.
2. Checks if the HEIF file size is larger than the JPEG file size. If it is, the JPEG file is removed.
3. Calculates and displays the count and space saved for each photo.
4. Calculates and displays the total count and space saved.

Usage:
    python heif_organizer.py <dir_path>

Arguments:
    dir_path (str): Path to the directory containing the photos.

Dependencies:
    - os
    - sys

Author: OpenAI
Date: May 15, 2023
Version: 1.1
"""

import os
import sys


def organize_photos(dir_path):
    total_count = 0
    total_space_saved = 0

    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            if filename.lower().endswith(".jpg"):
                jpg_path = os.path.join(root, filename)
                heif_path = os.path.join(root, f"{os.path.splitext(filename)[0]}.heif")

                if os.path.isfile(heif_path):
                    jpg_size = os.path.getsize(jpg_path)
                    heif_size = os.path.getsize(heif_path)

                    if heif_size < jpg_size:
                        os.remove(heif_path)
                        space_saved = 0  # No space saved when JPG file is kept
                        print(f"Deleted {heif_path} (Space Saved: {human_readable_size(space_saved)})")
                    elif heif_size > jpg_size:
                        os.remove(jpg_path)
                        space_saved = heif_size - jpg_size
                        total_space_saved += space_saved
                        print(f"Deleted {jpg_path} (Space Saved: {human_readable_size(space_saved)})")

                    total_count += 1

    print(f"Total Photos Processed: {total_count}")
    print(f"Total Space Saved: {human_readable_size(total_space_saved)}")


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
    organize_photos(dir_path)
