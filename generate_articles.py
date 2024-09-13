import os, shutil
import markdown, yaml
import re
from bs4 import BeautifulSoup
from generate_util import parse_markdown_article

def copy_images_and_update_links(src_file_path, html_file_path, assets_img_dir):
    """
    Copie les images du répertoire de l'article vers le répertoire /assets/images
    et met à jour les liens vers ces images dans le fichier HTML.
    """
    # Lire le contenu HTML généré
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    img_pattern =  r'images/[^/]+?\.(?:jpg|jpeg|png|heic)'
    imgs = re.findall(img_pattern, html_content, re.IGNORECASE)
    # remove duplicates in imgs
    imgs = list(set(imgs))

    # Le répertoire où sont les images d'origine (dans le même répertoire que le markdown)
    article_img_dir = os.path.dirname(src_file_path)

    for img_src in imgs:
        
        # Résoudre le chemin de l'image dans l'article
        original_img_path = os.path.join(article_img_dir, img_src)


        if os.path.exists(original_img_path):
            # Créer un nom d'image unique pour éviter les collisions
            unique_img_name = os.path.basename(src_file_path).replace('.html', '') + '_' + os.path.basename(img_src)

            # Chemin de destination dans /assets/images/
            new_img_path = os.path.join(assets_img_dir, unique_img_name)

            # Copier l'image vers /assets/images/
            shutil.copy2(original_img_path, new_img_path)

            rel_img_path = os.path.relpath(new_img_path, os.path.dirname(html_file_path))
            
            html_content = html_content.replace(img_src, rel_img_path)
            #html_content = html_content.replace(img_src, f'../../assets/images/{unique_img_name}')
        else:
            print(f"Image non trouvée : {original_img_path}")

    # Écrire le contenu HTML modifié
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        f.close()


    print(f"Liens d'images mis à jour et images copiées pour : {html_file_path}")


def process_articles(content_dir, html_dir, assets_img_dir):
    """
    Parcourt les articles dans /content/YYYY/MM/DD/xx-article/,
    copie les fichiers HTML dans /html/articles/ et les images dans /assets/images/.
    """
    # Créer les répertoires s'ils n'existent pas encore
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(assets_img_dir, exist_ok=True)

    # Parcourir les fichiers markdown dans content
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.html'):
                src_file_path = os.path.join(root, file)
                
                # Correspondre le chemin HTML de sortie avec le chemin markdown
                relative_path = os.path.relpath(root, content_dir)
                #html_articledir = os.path.join(html_dir, "articles")
                html_articledir = os.path.join(html_dir, relative_path)
                os.makedirs(html_articledir, exist_ok=True)

                # copy hml file in html dir
                # copy the images directory that contains the article images to the output directory
                #images_dir = os.path.join(os.path.dirname(src_file_path), 'images')
                #if os.path.exists(images_dir):
                #   shutil.copytree(images_dir, os.path.join(html_subdir, 'images'))
                # copy current file to html_subdir
                html_file_name = file
                html_file_path = os.path.join(html_articledir, html_file_name)
                shutil.copy2(src_file_path, html_file_path)

                # Copier les images et mettre à jour les liens dans le fichier HTML
                copy_images_and_update_links(src_file_path, html_file_path, assets_img_dir)
                

def generate_html_article(md_file_path, output_dir,prev_link="",next_link=""):
    """Génère un fichier HTML pour un article à partir d'un fichier markdown."""
    # Parse le fichier markdown pour obtenir les métadonnées et le contenu
    meta_data, md_content = parse_markdown_article(md_file_path)

    # Convertir le contenu markdown en HTML
    html_content = markdown.markdown(md_content)

    # Extraire les informations importantes des métadonnées
    title = meta_data.get('title', 'Titre de l\'article')
    collection = meta_data.get('tags', 'Autre')
    date = meta_data.get('date', 'Date inconnue')

    nav_links = ""
    if prev_link or next_link:
        nav_links = f"""
        <nav>
            {f'<a href="../../../../../{prev_link}">Article précédent</a>' if prev_link else ''}
            {f'<a href="../../../../../{next_link}">Article suivant</a>' if next_link else ''}
        </nav>
        """

    # Générer le template HTML pour l'article
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="../assets/css/style.css">
    </head>
    <body>
        <header>
            <h1>{title}</h1>
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

    # Générer le chemin de sortie pour le fichier HTML
    article_filename = os.path.basename(md_file_path).replace('.md', '.html')
    # articles are located in /path/to/YYYY/MM/DD/subdir/article.md
    # get articles subpath /YYYY/MM/DD/subdir/
    path_elems = md_file_path.split('/')
    path_elems.pop() # remove article.md
    # get last 4 elements
    path_elems = path_elems[-4:]
    subpath = '/'.join(path_elems)

    output_dir = os.path.join(output_dir, subpath)
    output_file_path = os.path.join(output_dir ,article_filename)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # copy the images directory that contains the article images to the output directory
    images_dir = os.path.join(os.path.dirname(md_file_path), 'images')
    # use shutil
    if os.path.exists(images_dir):
        shutil.copytree(images_dir, os.path.join(output_dir, 'images'))
    



    # Écrire le contenu HTML dans le fichier de sortie
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"Article HTML généré : {output_file_path}")

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

    process_articles(content_dir, html_dir, assets_img_dir)