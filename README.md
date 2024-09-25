# Set-up python environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Configuration
Blog root file is stored in .env file
```blog_url="https://myblog.blogger.com/"```

# Usage
There are 3 scripts to use in order
1. crawl_blog.py : get a list of blog post urls and store them in a file
2. scrapblog.py : using the file list of urls in input, download all posts in mardown format (images are also downloaded)
3. the blog can be generated again using generate_website.py script


# Crawl Blog Usage Guide

This script allows you to crawl a blog and retrieve URLs of blog posts.

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - python-dotenv

## Configuration

1. Create a `.env` file in the same directory as the script.
2. Add the following line to the `.env` file, replacing `<your-blog-url>` with your actual blog URL: blog_url="<your-blog-url>"


## Usage

Run the script using the following command:
```python crawl_blog.py -h -f FIRST_POST_URL -m MAX_POSTS -o OUTPUT```

### Arguments

- `-h`, `--help`: Show the help message and exit.
- `-f FIRST_POST_URL`, `--first_post_url FIRST_POST_URL`: URL of the first post to start crawling from.
- `-m MAX_POSTS`, `--max_posts MAX_POSTS`: Maximum number of posts to crawl (integer).
- `-o OUTPUT`, `--output OUTPUT`: Output file to save the crawled URLs.

### Examples

1. Crawl all posts starting from the blog URL specified in the `.env` file:
```python crawl_blog.py -f https://example.com/first-post -m 50```
2. Crawl and save URLs to a custom output file:
```python crawl_blog.py -o my_blog_urls.txt```
3. Combine multiple options:
```python crawl_blog.py -f https://example.com/start-here -m 100 -o recent_posts.txt```

## Notes

- If no `first_post_url` is provided via command line, the script will attempt to use the `blog_url` from the `.env` file.
- If no `max_posts` is specified, the script will attempt to crawl all available posts.
- The default output file is `all_urls.txt` if not specified.

## Output

The script will print progress information to the console and save the crawled URLs to the specified output file (or `all_urls.txt` by default).


# Scrapblog.py script Usage
To scrape your blog posts and save them locally, run the following command:
```python3 scrapblog.py -u <blog_url> -t <target_directory> -m <max_pages>```
- `-u`, `--blog_url`: The URL of the blog you want to scrape. This is a required argument.
- `-t`, `--target_directory`: The directory where the scraped blog posts will be saved as Markdown files. This is a required argument.
- `-m`, `--max_pages`: The maximum number of pages (blog posts) to scrape. If not provided, the script will scrape all available posts.

For example, to scrape the latest 50 posts from `https://myblog.example.com` and save them as Markdown files in the `~/blog-backup` directory, you would run:
```python scrapblog.py -u https://myblog.example.com -t ~/blog-backup -m 50```

The markdown files and images are stored in
```
MD_DIR/YYYY/MM/DD/XX-folder_name/post.md
MD_DIR/YYYY/MM/DD/XX-folder_name/images/*.jpg
```
The structure of the markdown file is composed of 
- a yaml block
- the main text
- an optionnal comment section that starts with "Commentaires"
```
---
title: Direction equateur - 8 juillet
date: lundi 10 juillet 2023
tags: equateur
---

My blog post
blabla

Commentaires:

Anonymous (10 juillet 2023 à 14:52):
Good job !

```

# Blog Generator

This project contains a Python script (`generate_website.py`) that generates a static website from Markdown files. It creates HTML articles, collection pages, and index pages for a blog-like structure.

## Usage

1. Ensure you have Python installed on your system.

2. Install the required dependencies (if any - you may need to create a `requirements.txt` file listing the dependencies).

3. Prepare your Markdown files:
   - Place all your Markdown (.md) files in a directory named `md` in the project root.
   - Each Markdown file should represent a blog post and include metadata (title, date, tags) at the top.

4. Run the script

5. The generated website will be created in the `html` directory.

## Directory Structure

After running the script, the following directory structure will be created:
```
html/
├── assets/
│ ├── css/
│ │ ├── style.css
│ │ ├── v0-article.css
│ │ ├── v0-article-black.css
│ │ └── v0-index.css
│ └── images/
├── articles/
│ └── generated HTML articles
├── collections/
│ └── generated collection pages
└── index.html
```

## Configuration

The script uses a configuration dictionary to manage various directories:

- `md_dir`: Directory containing Markdown files (default: 'md')
- `html_dir`: Output directory for the generated website (default: 'html')
- `assets_dir`: Directory for static assets (default: 'html/assets')
- `css_dir`: Directory for CSS files (default: 'html/assets/css')
- `img_dir`: Directory for images (default: 'html/assets/images')
- `articles_dir`: Directory for generated HTML articles (default: 'html/articles')
- `collections_dir`: Directory for generated collection pages (default: 'html/collections')

## Features

1. Generates individual HTML articles from Markdown files
2. Creates collection pages based on tags
3. Generates index pages
4. Supports navigation between articles (previous/next links)
5. Copies CSS files to the output directory

## The Role of tags.json
Tags are currently used to manage collections. Each article is associated to a collection, and a collection groups all articles containing this tag.


# TODO
Add parameters for "cache" directory, tags.json file
I18N : get rid of "Commentaires" in the code