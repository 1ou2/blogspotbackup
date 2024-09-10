# build a web scraper in python
import requests
from bs4 import BeautifulSoup
import markdownify
import urllib.request, urllib.parse, urllib.error
import re, os, sys,argparse

from dotenv import load_dotenv


def main():
    # default values
    target_directory = "md"
    max_pages = 3
    blog_url = ""

    # add three optional arguments, using argparse
    # -t target_directory where md files will be stored,
    # -m max_pages maximum number of pages to scrap,
    # -u blog_url
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target_directory", help="target directory where md files will be stored")
    parser.add_argument("-m", "--max_pages", type=int, help="maximum number of pages to scrap")
    parser.add_argument("-u", "--blog_url", help="blog url to scrap")
    args = parser.parse_args()
    if args.target_directory:
        target_directory = args.target_directory
    if args.max_pages:
        max_pages = args.max_pages
    if args.blog_url:
        blog_url = args.blog_url
        
    if blog_url == "":
        # load blog url from .env
        # Load environment variables from .env file
        load_dotenv()

        # Access the secret parameter
        blog_url = os.getenv("blog_url")
        if not blog_url:
            print("blog_url not found in .env file")
            sys.exit(1)
    
    print(f"Backuping: {blog_url}")
    print(f"target_directory: {target_directory}")
    print(f"max_pages: {max_pages}")

    # create a md directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created md directory: {target_directory}")

    
    nextpage = blog_url
    allurls = set()
    while nextpage and max_pages > 0:
        print(f"{max_pages=}, {nextpage=}")
        hrefs, nextpage = get_posts_url_from_page(nextpage)
        for h in hrefs:
            if h not in allurls:
                allurls.add(h)
                print(f"New url: {h}")
        print("----")
        max_pages -= 1

    print(f"Retreived : {len(allurls)=}")
    print("-------\n")

    stats = dict()
    for url in allurls:
        extract_post(url,stats)

    if stats:
        max_length = max(len(str(s)) for s in stats)
        for s in sorted(stats):
            print(f"{s:{max_length}d} : {stats[s]['url']}\n{stats[s]['path']}{stats[s]['filename']} - images {stats[s]['images']}\n")

#
# Returns all posts urls, and the next page blog as a tuple
# [url1, url2, ...], next_page_url
def get_posts_url_from_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text # gets you the text of the <title>(...)</title>
    print(f"url: {url}")

    
    # get all class='posts' inside archivedates
    posts = soup.find_all(class_='post-title')
    # extract all hrefs from the <a> tags
    hrefs = []
    for post in posts:
        a_tags = post.find_all('a')
        for a_tag in a_tags:
            hrefs.append(a_tag['href'])
    
    nextpage = soup.find_all(class_='blog-pager-older-link')
    if nextpage:
        nextpage = nextpage[0]["href"]
    return hrefs, nextpage



def extract_post(url,stats):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text # gets you the text of the <title>(...)</title>
    
    # get the filename from the link, and remove extension
    filename = url.split('/')[-1]
    # replace extension with .md
    filename = filename.replace('.html', '.md')

    # get url path and create directories
    path = "md/"+"/".join(url.split('/')[3:])
    # remove the extension from the path. Extension can be .html, .htm 
    path = path.replace('.html', '').replace('.htm', '') + "/"
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created {path}")
    else:
        print(f"Path {path} already exists, skipping...")
        return
    
    id = len(stats)
    stats[id] = {}
    stats[id]['url'] = url
    stats[id]['title'] = title
    stats[id]['path'] = path
    stats[id]['filename'] = filename
    # Get 'entry-content' from the html
    entry_content = soup.find(class_='entry-content')

    # entry_content is an html div
    # convert it to markdown
    # use a library like markdownify
    md_text = markdownify.markdownify(entry_content.decode_contents())
    # the markdown contains links to images
    # like :
    # [![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXza-U5b5yvxYQ/s320/IMG_3765.jpg)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEGLza-U5b5yvxYQ/s1154/IMG_3765.jpg)
    #
    # download preview image and fullres image
    # and replace the links with the local paths
    # use a library like urllib to download the images
    # and replace the links in the markdown with the local paths
    # use a library like re to replace the links

    # search images, images are [![](preview_url)]](fullres_url)
    images = re.findall(r'\[!\[\]\(.*?\)\]\(.*?\)', md_text)
    stats[id]['images'] = len(images)

    # download the images
    for image in images:
        preview_url = re.search(r'\[!\[\]\((.*?)\)\]\(.*?\)', image).group(1)
        fullres_url = re.search(r'\[!\[\]\(.*?\)\]\((.*?)\)', image).group(1)
        # download the preview image
        preview_name = "small_" + preview_url.split('/')[-1]
        urllib.request.urlretrieve(preview_url, path+preview_name)
        # download the full res image
        fullres_name = fullres_url.split('/')[-1]
        urllib.request.urlretrieve(fullres_url, path+fullres_name)
        # replace the links in the markdown
        md_text = md_text.replace(preview_url, preview_name)
        md_text = md_text.replace(fullres_url, fullres_name)

    # save the markdown to a file
    with open(path+filename, 'w') as f:
        f.write(md_text)
        

if __name__ == "__main__":    
    main()

