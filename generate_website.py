import os
import shutil
from generate_articles import generate_html_article, process_articles
from generate_collections import generate_collection_pages
from generate_index import generate_index_pages
from generate_util import clean_output_directory,get_sorted_articles


def create_website():
    # Define your directory paths
    blog_dir = 'blog'
    md_dir = 'md'
    content_dir = './blog/content'
    html_dir = './blog/html'
    assets_img_dir = './blog/assets/images'
    html_articles_dir = './blog/html/articles'
    html_collections_dir = './blog/html/collections'

    # Clean up the output directory
    clean_output_directory(blog_dir)

    articles = get_sorted_articles(md_dir)
    print(f"Found {len(articles)} articles.")

    alltags = set()
    for article in articles:
        alltags.add(article['tags'])

    # Step 1: Generate individual HTML articles
    output_dir = './blog/content/articles/'
    # articles are sorted
    # iterate though articles, get current, previous and next article
    for prev_article, article, next_article in zip([None] + articles[:-1], articles, articles[1:] + [None]):
        prev_link = "" 
        next_link = ""
        if prev_article:
            prev_link = prev_article['link']
        if next_article:
            next_link = next_article['link']
        md_file_path = article['file_path']
        generate_html_article(md_file_path, output_dir, prev_link, next_link)

    
    #for root, dirs, files in os.walk(md_dir):
    #    for file in files:
    #        if file.endswith('.md'):
    #            md_file_path = os.path.join(root, file)
    #            generate_html_article(md_file_path, output_dir)

    # Step 2: Process articles (copy and update image links)
    process_articles(content_dir, html_dir, assets_img_dir)

    # Step 3: Generate collection pages
    generate_collection_pages(md_dir, html_articles_dir, html_collections_dir)

    # Step 4: Generate the index page
    generate_index_pages(md_dir, html_dir,list(alltags))

    print("Website generated successfully!")
    print(articles)

if __name__ == "__main__":
    create_website()
