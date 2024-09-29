import os
from collections import defaultdict
from util_scrap import Cache

def count_files_by_extension(directory):
    file_counts = defaultdict(int)

    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()  # Get the file extension
            file_counts[ext] += 1  # Increment the count for this extension
            if ext == "":
                print(f"{root} {dirs} {file}")
            if ext.lower() == ".heic":
                print(f"{root} {dirs} {file}")
            if ext.startswith(".b"):
                print(f"{root} {dirs} {file}")

    return file_counts

def analyse_cache():
    cache = Cache(cache_dir="/home/gabriel/dev/blogspotbackup/cache")
    cache.load_cache()
    for url, filename in cache.cache.items():
        if filename.lower().endswith(".heic"):
            print(f"{url} {filename}")


def clear_heic_from_cache():
    cache = Cache(cache_dir="/home/gabriel/dev/blogspotbackup/cache")
    cache.load_cache()
    to_delete = []
    for url, filename in cache.cache.items():
        if filename.lower().endswith(".heic"):
            to_delete.append(url)
    for url in to_delete:
        print(f"Deleting {url} from cache : {filename}")
        del cache.cache[url]
    # save the cache
    cache.save_cache()

# Example usage
directory_path = "/home/gabriel/dev/_blogbackup/html"
file_counts = count_files_by_extension(directory_path)

# Print the results
for ext, count in file_counts.items():
    print(f"{ext}: {count}")

print("===")
analyse_cache()
print("===")
clear_heic_from_cache()

print("***")
analyse_cache()
print("***")
