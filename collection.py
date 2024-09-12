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

def generate_collection_pages(content_dir, html_articles_dir, html_collections_dir):
    """Génère les pages de collections basées sur les articles dans le répertoire content."""
    # Créer le répertoire des collections s'il n'existe pas encore
    os.makedirs(html_collections_dir, exist_ok=True)

    collections = {}

    # Parcourir tous les fichiers markdown
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)

                # Parse le fichier markdown pour obtenir les métadonnées
                meta_data = parse_markdown_article(md_file_path)

                # Récupérer la collection associée
                collection = meta_data.get('tags', 'Autre')
                title = meta_data.get('title', 'Titre de l\'article')

                # Créer le chemin relatif du fichier HTML de l'article
                relative_path = os.path.relpath(root, content_dir)
                html_article_path = os.path.join(html_articles_dir, relative_path, file.replace('.md', '.html'))

                # Ajouter l'article à la collection correspondante
                if collection not in collections:
                    collections[collection] = []
                collections[collection].append({
                    'title': title,
                    'link': os.path.relpath(html_article_path, html_collections_dir)  # Chemin relatif
                })

    # Générer les pages HTML pour chaque collection
    for collection, articles in collections.items():
        collection_file_path = os.path.join(html_collections_dir, f"{collection}.html")

        # Générer le contenu HTML pour la collection
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Collection: {collection}</title>
            <link rel="stylesheet" href="../assets/css/style.css">
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
            html_content += f'<li><a href="{article["link"]}">{article["title"]}</a></li>\n'

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

# Exemple d'utilisation
content_dir = './md'
html_articles_dir = './blog/html/articles'
html_collections_dir = './blog/html/collections'

generate_collection_pages(content_dir, html_articles_dir, html_collections_dir)
