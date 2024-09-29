import os, shutil
import markdown, yaml
import re
from bs4 import BeautifulSoup
from utils.generate_util import parse_markdown_article,get_image_names          

def generate_html_article(article, configuration, prev_link="",next_link=""):
    """Generate an HTML article file, from an article"""
    # Convertir le contenu markdown en HTML
    html_content = article['html_content']
    articles_dir = configuration['articles_dir']
    assets_img_dir = configuration['img_dir']
    css_dir = configuration['css_dir']

    # Extraire les informations importantes des métadonnées
    title = article.get('title', 'Titre de l\'article')
    collection = article.get('tags', 'Autre')
    date = article.get('date', 'Date inconnue')

    nav_links = ""
    if prev_link or next_link:
        nav_links = f"""
        <nav>
            {f'<a href="../../../../../{prev_link}">Article précédent</a>' if prev_link else ''}
            {f'<a href="../../../../../{next_link}">Article suivant</a>' if next_link else ''}
        </nav>
        """

    # Générer le chemin de sortie pour le fichier HTML
    md_file_path = article['file_path']
    # articles are located in /path/to/YYYY/MM/DD/subdir/article.md
    # get articles subpath /YYYY/MM/DD/subdir/
    path_elems = md_file_path.split('/')
    html_name = path_elems.pop().replace('.md', '.html') # article.html
    # html/articles/YYYY/MM/DD/subdir/     
    path_elems = path_elems[-4:] # get last 4 elements
    article_subdir = path_elems[-1]
    subpath = '/'.join(path_elems)

    # directory where the article will be saved
    article_dir = os.path.join(articles_dir, subpath)
    article_file_path = os.path.join(article_dir, html_name)

    if not os.path.exists(article_dir):
        os.makedirs(article_dir)

    # source directory for the images
    src_images_dir = os.path.join(os.path.dirname(md_file_path), 'images')
    # copy the images directory that contains the article images to the output directory
    for root, dirs, files in os.walk(src_images_dir):
        for file in files:
            original_img_path = os.path.join(root, file)
            # create a unique name for the images
            new_img_path = os.path.join(assets_img_dir, f"{article_subdir}_{file}")
            shutil.copy2(original_img_path, new_img_path)
    
    # modify the html content to point to the images in the assets directory
    image_names = get_image_names(html_content)
    for img_name in image_names:
        # img_name = "images/IMG_1234.jpg" -> get name part
        name = img_name.split('/')[1]
        rel_assets_img = os.path.relpath(assets_img_dir, article_dir)
        html_content = html_content.replace(img_name, os.path.join(rel_assets_img,f'{article_subdir}_{name}'))

    # add style to comments
    comments = html_content.split("<p>Commentaires:</p>")
    if len(comments) > 1:
        html_content = comments[0] + "<div class='comments'>\n" + "<h3>Commentaires:</h3>\n"+ comments[1] + "\n</div>"
        #print(html_content)

    article['html_content'] = html_content

    index_rel_path = "../../../../.."
    theme = configuration['theme']
    css_rel_path = os.path.relpath(os.path.join(css_dir,f"article-{theme}.css"), article_dir)
    # Générer le template HTML pour l'article
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="{css_rel_path}">
    </head>
    <body>
        <header>
            <h1>{title}</h1>
            <nav>
                <ul>
                    <li><a href="{index_rel_path}/index.html">Accueil</a></li>
                    <li><a href="{index_rel_path}/collections/">Collections</a></li>
                    {f'<li><a href="../../../../../{prev_link}">Article précédent</a></li>' if prev_link else ''}
                    {f'<li><a href="../../../../../{next_link}">Article suivant</a></li>' if next_link else ''}
                    <li><a href="{index_rel_path}/about.html">À propos</a></li>
                </ul>
            </nav>
            <p><em>Publié le {date} | Collection : {collection}</em></p>
        </header>
        <main>
            {html_content}
        </main>
        <footer>
            {nav_links}
            <p><a href="../../../../../index.html">Retour à la page principale</a></p>
            <p><a href="../../../../../collections/{collection}.html">Voir tous les articles de {collection}</a></p>
        </footer>
    </body>
    </html>
    """

    # Écrire le contenu HTML dans le fichier de sortie
    with open(article_file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"Article HTML généré pour : {md_file_path}")


if __name__ == "__main__":
    blog_dir = 'blog'
    md_dir = 'md'
    # clean-up : remove html dir
    if os.path.exists(blog_dir):
        shutil.rmtree(blog_dir)
    output_dir = './blog/content/articles/'
    for root, dirs, files in os.walk(md_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                generate_html_article(md_file_path, output_dir)

    content_dir = './blog/content'
    html_dir = './blog/html'
    assets_img_dir = './blog/assets/images'