output_dir="./compressed"
mkdir -p "$output_dir"

timing_file="./compression_times.txt"
echo "Image, Compression Factor, Method, Time (sec)" > "$timing_file"

for image in ./imgs/*; do
    for c in 1 3 10; do
        for m in numpy simple advanced; do
            echo "Compressing $image with method $m and compression factor $c..."
            compression_time=$( (time -p python main.py --mode=compress --method="$m" --input="$image" --output="/tmp/tmp.svdi" --compression="$c") 2>&1 | grep real | awk '{print $2}')
            
            echo "${image##*/}, $c, $m, $compression_time" >> "$timing_file"

            python main.py --mode=decompress --input="/tmp/tmp.svdi" --output="$output_dir/${c}.${m}.${image##*/}"
        done
    done
done
