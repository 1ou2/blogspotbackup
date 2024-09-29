# build a web scraper in python
import requests
from bs4 import BeautifulSoup
import markdownify
import urllib.request, urllib.parse, urllib.error
import re, os, sys,argparse

from dotenv import load_dotenv

"""
Get all posts urls from a blog page
"""
def get_urls(blog_url,max_pages):
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

def get_first_post_url():
    load_dotenv()
    first_post_url = ""
    blog_url = os.getenv("blog_url")
    if not blog_url:
        print("blog_url not provided")
        sys.exit(1)

    urls, nextpage = get_posts_url_from_page(blog_url)

    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        previous_page = soup.find_all(class_='blog-pager-newer-link')
        if not previous_page:
            print(f"found first post: {url}")
            return url
        else:
            print(f"discarded {url}")
    
    return None
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

def get_ordered_posts(firstpost_url,max=None):
    posts = []
    nextpost = firstpost_url

    while nextpost and (max ==None or max >0):
        if max != None:
            max = max -1
        if len(posts) % 10 == 0:
            print(f"{len(posts)=}, {nextpost=}")
        posts.append(nextpost)
        soup = BeautifulSoup(requests.get(nextpost).text, 'html.parser')
        nextpost = soup.find_all(class_='blog-pager-older-link')
        if nextpost:
            nextpost = nextpost[0]["href"]
    return posts

def main():
    # default values
    output = "all_urls.txt"
    max_posts = None
    first_post_url = None
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--first_post_url", help="url of the first post")
    parser.add_argument("-m", "--max_posts", type=int, help="maximum number of posts to crawl")
    parser.add_argument("-o", "--output", help="output file")
    args = parser.parse_args()

    if args.first_post_url:
        first_post_url = args.first_post_url
    if args.max_posts:
        max_posts = args.max_posts
    if args.output:
        output = args.output

    if not first_post_url:
        # load blog url from .env
        load_dotenv()
        first_post_url = os.getenv("first_post_url")
        if not first_post_url:
            print("first_post_url not provided")
            first_post_url = get_first_post_url()
            if not first_post_url:
                print("Could not find first post url")
                sys.exit(1)

    print(f"output file {output}")
    print(f"Crawling from {first_post_url} with max {max_posts}")
    posts = get_ordered_posts(first_post_url,max_posts)
    print(f"Crawled : {len(posts)}")

    # write all urls to a file
    with open(output, "w") as f:
        for post in posts:
            f.write(post + "\n")



if __name__ == "__main__":    
    main()

