import os
import yaml
import markdown

def parse_markdown_article(md_file_path):
    """Parse le fichier markdown pour extraire les métadonnées et le contenu."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # Séparer l'en-tête YAML du contenu markdown
        if content.startswith('---'):
            _, meta_data, _ = content.split('---', 2)
            meta_data = yaml.safe_load(meta_data)
        else:
            meta_data = {}

        return meta_data

def generate_collection_pages(articles, configuration, collections):
    """Génère les pages de collections basées sur les articles dans le répertoire content."""
   
    # Générer les pages HTML pour chaque collection
    for collection in collections:

        collection_file_path = os.path.join(configuration['collections_dir'], f"{collection}.html")

        # Générer le contenu HTML pour la collection
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Collection: {collection}</title>
            <link rel="stylesheet" href="../assets/css/v0-index.css">
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
            if article['tags'] == collection:
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

if __name__ == "__main__":
    # Exemple d'utilisation
    content_dir = './md'
    html_articles_dir = './blog/html/articles'
    html_collections_dir = './blog/html/collections'

    generate_collection_pages(content_dir, html_articles_dir, html_collections_dir)
