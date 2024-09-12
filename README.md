# Set-up python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configuration
Blog root file is stored in .env file
```blog_url="https://myblog.blogger.com/"```

# Usage
To scrape your blog posts and save them locally, run the following command:
```python3 scrapblog.py -u <blog_url> -t <target_directory> -m <max_pages>```
- `-u`, `--blog_url`: The URL of the blog you want to scrape. This is a required argument.
- `-t`, `--target_directory`: The directory where the scraped blog posts will be saved as Markdown files. This is a required argument.
- `-m`, `--max_pages`: The maximum number of pages (blog posts) to scrape. If not provided, the script will scrape all available posts.

For example, to scrape the latest 50 posts from `https://myblog.example.com` and save them as Markdown files in the `~/blog-backup` directory, you would run:
```python scrapblog.py -u https://myblog.example.com -t ~/blog-backup -m 50```


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


