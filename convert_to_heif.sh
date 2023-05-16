#!/bin/bash

#######################################################################
# Script: jpeg_to_heic_conversion.sh                                  #
# Description: Converts JPEG images to HEIC format and calculates     #
#              the space saved by the conversion.                     #
# Usage: jpeg_to_heic_conversion.sh <input_directory>                 #
# Author: K H M BURHAN UDDIN                                          #
# Date: May 12, 2023                                                  #
# Version: 1.3                                                        #
#######################################################################

# Script Summary:
# This script converts JPEG images in the specified directory to HEIC format,
# resizes them to 4000x3000 pixels if larger, and copies metadata from the original
# images. It calculates the space saved by the conversion and displays the original
# and converted file sizes. The original JPEG images are deleted after conversion.

# Usage:
# Execute the script by providing the input directory as a command-line
# argument. For example:
#     bash jpeg_to_heic_conversion.sh /path/to/directory

# Author: K H M BURHAN UDDIN

# Date: May 12, 2023

# Version: 1.3

# Dependencies:
# - ImageMagick (convert command)
# - exiftool
# - stat command

#######################################################################

input_dir="$1"

# Check if input directory is provided
if [ -z "$input_dir" ]; then
    echo "Please provide the input directory as a command-line argument."
    exit 1
fi

# Find all JPEG files recursively in the input directory
jpg_images=($(find "$input_dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" \)))
total_images=${#jpg_images[@]}

current_image=0
original_total_size=0
converted_total_size=0
progress_file="$input_dir/heic.log.csv"

# Check if progress file exists
if [ -f "$progress_file" ]; then
    # Read the progress file and retrieve processed files and sizes
    while IFS=, read -r file_path original_size converted_size; do
        processed_files+=("$file_path")
        original_total_size=$((original_total_size + original_size))
        converted_total_size=$((converted_total_size + converted_size))
    done < "$progress_file"
else
    processed_files=()
fi

for jpg_image in "${jpg_images[@]}"; do
    # Check if the file has already been processed
    if [[ "${processed_files[*]}" =~ "$jpg_image" ]]; then
        echo "Skipping already processed file: $jpg_image"
        continue
    fi

    current_image=$((current_image + 1))

    # Get the filename without extension
    filename=$(basename "$jpg_image")
    extension="${filename##*.}"
    filename="${filename%.*}"

    echo "Processing image $current_image of $total_images: $jpg_image"

    # Define the output HEIC file path
    output_file="${jpg_image%.*}.heic"

    # Run the conversion command
    convert "$jpg_image" -resize 4000x3000 "$output_file"
    exiftool -TagsFromFile "$jpg_image" -all:all "$output_file"

        # Get the sizes of the original and converted files
    original_size=$(stat -c%s "$jpg_image")
    converted_size=$(stat -c%s "$output_file")

    echo "Original size: $(numfmt --to=iec-i --suffix=B "$original_size")"
    echo "Converted size: $(numfmt --to=iec-i --suffix=B "$converted_size")"
    echo "------------------------------"

    # Store the processed file path, original size, and converted size in the progress file as CSV
    echo "$jpg_image,$original_size,$converted_size" >> "$progress_file"

    # Increment the total sizes
    original_total_size=$((original_total_size + original_size))
    converted_total_size=$((converted_total_size + converted_size))

    # Set the file created and modified dates to match the original file
    original_date=$(stat -c %y "$jpg_image")
    touch -r "$jpg_image" -d "$original_date" "$output_file"

    # Delete the original .heic_original file
    rm -f "${output_file}_original"

    # Sleep for one second
    sleep 1
done

# Remove the progress file if all images have been processed
# if [ "${#jpg_images[@]}" -eq "$current_image" ]; then
#     rm -f "$progress_file"
# fi

# Calculate the space saved
space_saved=$((original_total_size - converted_total_size))

echo "Conversion completed!"
echo "Total original size: $(numfmt --to=iec-i --suffix=B "$original_total_size")"
echo "Total converted size: $(numfmt --to=iec-i --suffix=B "$converted_total_size")"
echo "Space saved: $(numfmt --to=iec-i --suffix=B "$space_saved")"


