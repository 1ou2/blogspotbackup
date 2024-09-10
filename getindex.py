# build a web scraper in python
import requests
from bs4 import BeautifulSoup

import markdownify
import urllib.request
import urllib.parse
import urllib.error
import re
import os
from dotenv import load_dotenv

class Post:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.date = None
        self.content = None
        self.images = []
        self.previews = []

    def __str__(self):
        return f"{self.title}\n{self.date}\n{self.content}"
    
def main():
    # load blog url from .env
    # Load environment variables from .env file
    load_dotenv()

    # Access the secret parameter
    blog_url = os.getenv("blog_url")
    print(f"Backuping: {blog_url}")


    # create a md directory if it doesn't exist
    if not os.path.exists('md'):
        os.makedirs('md')
        print("Created md directory")

    maxpage = 1
    nextpage = blog_url
    allurls = set()
    while nextpage and maxpage > 0:
        print(f"{maxpage=}, {nextpage=}")
        hrefs, nextpage = get_posts_url_from_page(nextpage)
        for h in hrefs:
            if h not in allurls:
                allurls.add(h)
                print(f"New url: {h}")
        print("----")
        maxpage -= 1

    print(f"Retreived : {len(allurls)=}")
    print("-------\n")

    stats = dict()
    for url in allurls:
        extract_post(url,stats)

    for s in stats:
        print(f"{stats[s]['title']}\n{stats[s]['url']}\n{stats[s]['path']}{stats[s]['filename']}\n")

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
    id = len(stats)
    stats[id] = {}
    stats[id]['url'] = url
    stats[id]['title'] = title

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

