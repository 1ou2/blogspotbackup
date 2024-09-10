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