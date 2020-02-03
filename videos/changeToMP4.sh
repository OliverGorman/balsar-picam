for file in *.h264; do
    mv "$file" "$(basename "$file" .h264).mp4"
done
