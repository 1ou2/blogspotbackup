import urllib.request, urllib.parse, urllib.error
import re, os, sys,argparse,json
from PIL import Image
import pyheif

class Cache:
    def __init__(self, cache_dir="cache",cache_file="cache.json"):
        self.cache_dir = cache_dir
        self.cache_file = cache_file
        self.images_dir = cache_dir + "/images/"
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        self.cache = self.load_cache()

    # the cache dir stores
    # - cache.json file : association between a url and an unique image file
    # - an images/ dir containing all previously downloaded images. Image filename is unique 
    def load_cache(self):
        try:
            with open(os.path.join(self.cache_dir, self.cache_file), 'r') as f:
                cache = json.load(f)
                return cache
            # return json.load(f)
        except FileNotFoundError:
            return {}

    def save_cache(self):
        with open(os.path.join(self.cache_dir,self.cache_file), 'w') as f:
            json.dump(self.cache, f)

    def is_file_in_cache(self,filename):
        return filename in self.cache.values()
    
    def is_url_in_cache(self, url):
        filename = self.cache.get(url,None)
        if filename:
            if os.path.isfile(os.path.join(self.images_dir, filename)):
                return True
            else:
                print(f"File {filename} not found in cache")
                del self.cache[url]
                self.save_cache()
        return False
    
    def convert_heic_to_jpg(self,heic_file_path, jpg_file_path):
        print(f"Converting {heic_file_path} to {jpg_file_path}")
        # Open the HEIC file using pyheif
        heif_file = pyheif.read(heic_file_path)

        # Convert the HEIC data to a Pillow image
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        # Save the image as a JPG
        image.save(jpg_file_path, "JPEG")

    def add_file(self, url, filename):
        heic_filename = None
        # check if url is already in cache
        if not self.is_url_in_cache(url):
            # check if file is in HEIC format
            if UrlChecker(url).has_extension() and url.split('.')[-1].lower() == "heic":
                heic_filename = filename
                filename = filename.split('.')[0] + ".jpg"

            # filename contains a jpg extension, add a "_" prefix to the filename until it's unique
            while self.is_file_in_cache(filename):
                filename = "_" + filename

            if heic_filename:
                # download heic file
                urllib.request.urlretrieve(url, os.path.join(self.cache_dir, "images", heic_filename))
                try:
                    # convert heic to jpg
                    self.convert_heic_to_jpg(os.path.join(self.cache_dir, "images", heic_filename), os.path.join(self.cache_dir, "images", filename))
                except:
                    # not a real heic file, just rename the file assuming it is a jpeg
                    os.rename(os.path.join(self.cache_dir, "images", heic_filename), os.path.join(self.cache_dir, "images", filename))
            else:
                urllib.request.urlretrieve(url, os.path.join(self.cache_dir, "images", filename))
            self.cache[url] = filename
            self.save_cache()

    def get_filepath(self, filename):
        return os.path.join(self.images_dir, filename)
    
    def get_filename(self, url):
        return self.cache.get(url, None)

class UrlChecker:
    def __init__(self, url):
        self.url = url

    def is_image_url(self):
        # Define a regular expression pattern to match common image file extensions
        image_extensions = r'\.(jpg|jpeg|png|gif|bmp|heic)$'
        
        # Use the re.search() function to check if the URL matches the pattern
        if re.search(image_extensions, self.url, re.IGNORECASE):
            return True
        else:
            return False

    # check if the url ends with an extension
    def has_extension(self,):
        return '.' in self.url.split('/')[-1]
    
if __name__ == "__main__":
    cache = Cache()

    for url, filename in cache.cache.items():
        print(f"checking {filename}")
        if not filename:
            print(f"Deleting {url} from cache : no filename")
            del cache.cache[url]
        # check if the file exists
        if not os.path.isfile(os.path.join(cache.images_dir, filename)):
            print(f"Deleting {url} from cache  : file not found")
            del cache.cache[url]

    cache.save_cache()