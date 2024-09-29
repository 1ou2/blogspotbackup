import os
import yaml
import markdown

def generate_collection_index(configuration, collections):
    """Generate the index.html page for collections"""

    theme = configuration['theme']
    collections_dir = configuration['collections_dir']

    # Générer le contenu HTML pour l'index des collections
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Index des collections</title>
        <link rel="stylesheet" href="../assets/css/index-{theme}.css">
    </head>
    <body>
        <header>
            <h1>Nos voyages</h1>
        </header>
        <main>
            <div class="article article-list">
            <ul>
    """

    # Ajouter la liste des collections
    for collection in collections:
        html_content += f"<li><a href=\"{collection}.html\">{collection}</a></li>"

    html_content += """
            </ul>
            </div>
        </main>
        <footer>
            <p><a href="../index.html">Retour à la page principale</a></p>
        </footer>
    </body>
    </html>
    """

    # Écrire le fichier HTML de l'index des collections
    index_file_path = os.path.join(collections_dir, 'index.html')
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Page HTML générée pour l'index des collections : {index_file_path}")

def generate_collection_pages(articles, configuration, collections):
    """Generate HTML collection pages"""
   
    # Generate HTML page for each collection
    for collection in collections:

        collection_file_path = os.path.join(configuration['collections_dir'], f"{collection}.html")
        theme = configuration['theme']

        # Générer le contenu HTML pour la collection
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Collection: {collection}</title>
            <link rel="stylesheet" href="../assets/css/index-{theme}.css">
        </head>
        <body>
            <header>
                <h1>Collection : {collection}</h1>
                <p>Articles liés à ce voyage :</p>
            </header>
            <main>
                <ul>
        """
        # Ajouter la liste des articles dans cette collection
        for article in articles:
            art_col = f"{article['date'].year}-{article['tags']}"
            if art_col == collection:
                html_content += f"<li><a href=\"../{article['link']}\">{article['title']}</a></li>"
            

        html_content += """
                </ul>
            </main>
            <footer>
                <p><a href="../index.html">Retour à la page principale</a></p>
            </footer>
        </body>
        </html>
        """

        # Écrire le fichier HTML de la collection
        with open(collection_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Page HTML générée pour la collection : {collection_file_path}")

        generate_collection_index(configuration, collections)

if __name__ == "__main__":
    # Exemple d'utilisation
    content_dir = './md'
    html_articles_dir = './blog/html/articles'
    html_collections_dir = './blog/html/collections'

    generate_collection_pages(content_dir, html_articles_dir, html_collections_dir)
