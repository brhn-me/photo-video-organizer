import os
import sys
import datetime

def update_created_date(path):
    """
    Recursively updates the "created" date of all .mp4 files to their "modified" date.

    Args:
        path (str): The root directory path.

    Returns:
        None
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(root, file)
                modified_date = os.path.getmtime(file_path)
                modified_datetime = datetime.datetime.fromtimestamp(modified_date)
                accessed_date = os.path.getatime(file_path)
                accessed_datetime = datetime.datetime.fromtimestamp(accessed_date)
                created_date = os.path.getctime(file_path)
                created_datetime = datetime.datetime.fromtimestamp(created_date)

                # Skip files where the modified date is already the same as the created date
                if modified_datetime == created_datetime:
                    continue

                # Update the created date to match the modified date
                os.utime(file_path, (accessed_date, modified_date))
                print(f"Updated created date of '{file}' to {modified_datetime}")

if len(sys.argv) < 2:
    print("Please provide the directory path as a command-line argument.")
else:
    root_directory = sys.argv[1]
    update_created_date(root_directory)
