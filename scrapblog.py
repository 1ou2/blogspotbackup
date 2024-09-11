# build a web scraper in python
import requests
from bs4 import BeautifulSoup
import markdownify
import urllib.request, urllib.parse, urllib.error
import re, os, sys,argparse

from dotenv import load_dotenv

def is_image_url(url):
    # Define a regular expression pattern to match common image file extensions
    image_extensions = r'\.(jpg|jpeg|png|gif|bmp|heic)$'
    
    # Use the re.search() function to check if the URL matches the pattern
    if re.search(image_extensions, url, re.IGNORECASE):
        return True
    else:
        return False


def get_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    return urls

def main():
    # default values
    target_directory = ""
    urls_file = "test.txt"
    max_urls = 10

    # add three optional arguments, using argparse
    # -t target_directory where md files will be stored,
    # -m max_urls maximum number of pages to scrap,
    # -u blog_url
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target_directory", help="target directory where md files will be stored")
    parser.add_argument("-f", "--urls_file", help="urls to scrap")
    parser.add_argument("-m", "--max_urls", type=int, help="maximum number of urls to scrap")
    args = parser.parse_args()
    if args.target_directory:
        target_directory = args.target_directory
    else:
        target_directory = "md"
    if args.urls_file:
        urls_file = args.urls_file
    if urls_file == "":
        # load blog url from .env
        # Load environment variables from .env file
        load_dotenv()

        # Access the secret parameter
        urls_file = os.getenv("urls_file")
        if not urls_file:
            print("urls_file not found in .env file")
            sys.exit(1)
    if args.max_urls:
        max_urls = args.max_urls
        

    target_directory = "ttt"
    print(f"Backuping: {urls_file}")
    print(f"target_directory: {target_directory}")
    print(f"max_urls: {max_urls}")

    # create a md directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created md directory: {target_directory}")

    allurls = get_urls_from_file(urls_file)

    stats = dict()
    nb_extracted = 0
    for url in allurls:
        if extract_post(url,stats,mddir=target_directory):
            nb_extracted += 1
            if max_urls > 0 and nb_extracted >= max_urls:
                break
            if nb_extracted % 4 == 0:
                print(f"Processed {nb_extracted} urls - last url: {url}")

    if stats:
        max_length = max(len(str(s)) for s in stats)
        for s in sorted(stats):
            print(f"{s:{max_length}d} : {stats[s]['date']} {stats[s]['path']}{stats[s]['filename']}")


def extract_post(url,stats,mddir="md"):
    md_dir = mddir + "/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text # gets you the text of the <title>(...)</title>
    

    md_text = ""
    date_entry = soup.find(class_='date-header')
    if date_entry:
        date_entry = date_entry.get_text(strip=True)
        md_text += f"# {date_entry}\n"
        # date is in french format, 
        # e.g. jeudi 3 août 2023, convert it to 2023/08/03/
        date_parts = date_entry.split()
        day = date_parts[1]
        # add a leading zero if needed
        if len(day) == 1:
            day = "0" + day
        months = {"janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","août":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}
        month = months[date_parts[2]]
        year = date_parts[3]
        
    # get the filename from the link
    filename = url.split('/')[-1]
    # replace extension with .md
    filename = filename.replace('.html', '.md')

    path = md_dir + "/".join([year,month,day]) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    # get number of files in path directory
    entries = os.listdir(path)
    dirs = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    # check if we already have a directory ending with filename
    for d in dirs:
        if d.endswith(filename.replace('.md', '')):
            print(f"File already exists: {path+d}/{filename}")
            return False

    # Count the number of directories
    num_dirs = len(dirs)

    # prefix filename with the number of files
    dirname = str(num_dirs).zfill(2)+"-"+filename.replace('.md', '')+"/"
    
    # get url path and create directories
    path = path + dirname
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"File already exists: {path+dirname}")
        return False
    
    id = len(stats)
    stats[id] = {}
    stats[id]['url'] = url
    stats[id]['date'] = f"{year}/{month}/{day}"
    stats[id]['title'] = title
    stats[id]['path'] = path
    stats[id]['filename'] = filename


    # Get 'entry-content' from the html
    entry_content = soup.find(class_='entry-content')

    # entry_content is an html div
    # convert it to markdown
    # use a library like markdownify
    md_text += markdownify.markdownify(entry_content.decode_contents())

    # get comment-author and comment-body that are in the same comment-block
    
    # Find the dl element with the ID 'comment-blocks'
    comment_blocks = soup.find('dl', {'id': 'comments-block'})
    comment_elements= []
    if comment_blocks:
        # Iterate over the dt (comment-author) and dd (comment-body) elements
        
        author_elements = comment_blocks.find_all('dt',class_='comment-author')
        body_elements = comment_blocks.find_all('dd',class_='comment-body')
        date_elements = comment_blocks.find_all('dd',class_='comment-footer')
        for aut, bd, ts in zip(author_elements,body_elements,date_elements):
            author = aut.get_text(strip=True).replace('a dit…', '').rstrip()
            body = bd.get_text(strip=True)
            timestamp = ts.get_text(strip=True)
            comment_elements.append((author, body,timestamp))

        if comment_elements:
            # add comments to the markdown
            md_text += "\n\nCommentaires:\n"
            for author, body, timestamp in comment_elements:
                md_text += f"\n{author} ({timestamp}):\n{body}\n"
                # add a line break after each comment
                md_text += "\n"

    
    print(f"{md_text}")
    # Regular expression pattern to match URLs starting with "https://" until we get to a )
    # notice the +? : which requires the match to be non greedy and stop at the first )
    pattern = r'(https?://[^\s]+?)\)'

    # Find all matches
    urls = re.findall(pattern, md_text)
    images = []
    downloaded = []
    # Print the URLs
    for url in urls:
        print(f"URL: {url}")
        if url in downloaded:
            continue
        # some URL are very long and end with a /
        if url.endswith('/') or is_image_url(url):
            if url.endswith('/'):
                newurl = url[:-1]
                image_name = newurl.split('/')[-1] + ".jpg"
            else:
                image_name = url.split('/')[-1]
            if len(image_name) > 30:
                # get last 30 characters
                image_name = image_name[-30:]
            if image_name in images:
                image_name = "big_" + image_name
            images.append(image_name)
            urllib.request.urlretrieve(url, path + image_name)
            downloaded.append(url)
            md_text = md_text.replace(url, image_name)
        else:
            print(f"URL NOT IMAGE: {url}")

    # save the markdown to a file
    with open(path+filename, 'w') as f:
        f.write(md_text)

    return True  

if __name__ == "__main__":    
    main()

