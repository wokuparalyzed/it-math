#!/bin/bash

# Ensure the output directory exists
output_dir="./compressed"
mkdir -p "$output_dir"

# File to store the timing results
timing_file="./compression_times.txt"
echo "Image, Compression Factor, Method, Time (sec)" > "$timing_file"

# Iterate over all images in the 'images' folder
for image in ./imgs/*; do
    # Iterate over different compression factors
    for c in 1 3 10; do
        # Iterate over the three SVD methods
        for m in numpy simple advanced; do
            # Measure time for compression using 'time'
            echo "Compressing $image with method $m and compression factor $c..."
            compression_time=$( (time -p python main.py --mode=compress --method="$m" --input="$image" --output="/tmp/tmp.svdi" --compression="$c") 2>&1 | grep real | awk '{print $2}')
            
            # Save the time result to the timing file
            echo "${image##*/}, $c, $m, $compression_time" >> "$timing_file"

            # Decompress and save the result in the output folder
            python main.py --mode=decompress --input="/tmp/tmp.svdi" --output="$output_dir/${c}.${m}.${image##*/}"
        done
    done
done

echo "Processing complete. Compressed images are stored in the $output_dir directory."
echo "Timing results saved in $timing_file."
