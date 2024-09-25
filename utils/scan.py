import os
from collections import defaultdict

def count_files_by_extension(directory):
    file_counts = defaultdict(int)

    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()  # Get the file extension
            file_counts[ext] += 1  # Increment the count for this extension
            if ext == "":
                print(f"{root} {dirs} {file}")

    return file_counts

# Example usage
directory_path = "/home/gabriel/dev/blogspotbackup/md"
file_counts = count_files_by_extension(directory_path)

# Print the results
for ext, count in file_counts.items():
    print(f"{ext}: {count}")
