import os
import shutil
from utils.generate_articles import generate_html_article
from utils.generate_collections import generate_collection_pages
from utils.generate_index import generate_index_pages
from utils.generate_util import clean_and_create_dirs,get_sorted_articles


def create_website():
    md_dir = 'md'
    html_dir = 'html'
    assets_dir = os.path.join(html_dir,'assets')
    css_dir = os.path.join(assets_dir, 'css')
    img_dir = os.path.join(assets_dir, 'images')
    articles_dir = os.path.join(html_dir, 'articles')
    collections_dir = os.path.join(html_dir, 'collections')

    configuration = {
        'md_dir': md_dir,
        'html_dir': html_dir,
        'assets_dir': assets_dir,
        'css_dir': css_dir,
        'img_dir': img_dir,
        'articles_dir': articles_dir,
        'collections_dir': collections_dir
    }

    all_dirs = [html_dir, assets_dir, css_dir, img_dir, articles_dir, collections_dir]
    # Clean up the output directory
    clean_and_create_dirs(all_dirs)

    # copy CSS assets
    css_files = ['./style.css','v0-article.css','v0-article-black.css','v0-index.css']
    for css_file in css_files:
        shutil.copy2(f"assets/{css_file}", css_dir)

    articles = get_sorted_articles(md_dir)
    print(f"Found {len(articles)} articles.")

    alltags = set()
    for article in articles:
        alltags.add(article['tags'])

    # Step 1: Generate individual HTML articles
    # articles are sorted
    # iterate though articles, get current, previous and next article
    for prev_article, article, next_article in zip([None] + articles[:-1], articles, articles[1:] + [None]):
        prev_link = "" 
        next_link = ""
        if prev_article:
            prev_link = prev_article['link']
        if next_article:
            next_link = next_article['link']
        generate_html_article(article, configuration, prev_link, next_link)


    # Step 3: Generate collection pages
    #generate_collection_pages(md_dir, html_articles_dir, html_collections_dir)

    # Step 4: Generate the index page
    generate_index_pages(articles, html_dir,list(alltags))

    print("Website generated successfully!")

if __name__ == "__main__":
    create_website()