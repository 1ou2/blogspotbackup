import os
import math
import yaml
from datetime import datetime

def parse_markdown_metadata(md_file_path):
    """Récupère les métadonnées d'un fichier markdown."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            _, meta_data, _ = content.split('---', 2)
            meta_data = yaml.safe_load(meta_data)
            return meta_data
    return {}

def generate_index_pages(content_dir, html_dir, collections, articles_per_page=10):
    """Génère la page d'index du blog avec pagination."""
    # Créer le répertoire html s'il n'existe pas encore
    os.makedirs(html_dir, exist_ok=True)

    articles = []

    # Parcourir les articles et extraire les métadonnées
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                meta_data = parse_markdown_metadata(md_file_path)
                #date_str = meta_data.get('date', '1970-01-01')
                #date = datetime.strptime(date_str, '%Y-%m-%d')
                title = meta_data.get('title', 'Sans titre')
                #article_relative_path = os.path.relpath(os.path.join(html_dir, root, file.replace('.md', '.html')), html_dir + '/articles')
                article_relative_path = root.split('/')
                article_relative_path = os.path.join('articles','/'.join(article_relative_path[-4:]),file.replace('.md','.html'))
                # date can be extract from current directory
                current_path = article_relative_path.split('/')

                # remove the last element (the file name)
                current_path.pop()
                # remove article folder
                folder = current_path.pop()
                # folder starts with two digits, use them as the hour
                hour = folder[:2]
                # last 3 elements are the date
                date = datetime.strptime('/'.join(current_path[-3:]) + f":{hour}", '%Y/%m/%d:%H')

                articles.append({
                    'title': title,
                    'date': date,
                    'link': article_relative_path
                })

    # Trier les articles par date décroissante (plus récents d'abord)
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)

    # Pagination
    total_pages = math.ceil(len(articles) / articles_per_page)

    for page_num in range(1, total_pages + 1):
        page_file = os.path.join(html_dir, f'index{"" if page_num == 1 else f"_{page_num}"}.html')
        
        # Générer le contenu de la page
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Blog - Page {page_num}</title>
            <link rel="stylesheet" href="assets/css/style.css">
        </head>
        <body>
            <header>
                <h1>Mon Blog de Voyage</h1>
                <nav>
                    <ul>
                        <li><a href="index.html">Accueil</a></li>
                        <li><a href="#collections">Collections</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <h2>Articles récents - Page {page_num}</h2>
                <ul>
        """

        # Ajouter les articles de cette page
        start_idx = (page_num - 1) * articles_per_page
        end_idx = start_idx + articles_per_page
        for article in articles[start_idx:end_idx]:
            html_content += f'<li><a href="{article["link"]}">{article["title"]} ({article["date"].strftime("%d %B %Y")})</a></li>\n'

        html_content += """
                </ul>
        """

        # Ajouter les liens de pagination
        html_content += '<nav aria-label="Pagination"><ul class="pagination">\n'
        if page_num > 1:
            html_content += f'<li><a href="index_{page_num - 1}.html">Précédent</a></li>\n'
        if page_num < total_pages:
            html_content += f'<li><a href="index_{page_num + 1}.html">Suivant</a></li>\n'
        html_content += '</ul></nav>\n'

        # Ajouter la section des collections
        html_content += """
            <section id="collections">
                <h2>Collections</h2>
                <ul>
        """
        for collection in collections:
            html_content += f'<li><a href="collections/{collection}.html">{collection}</a></li>\n'

        html_content += """
                </ul>
            </section>
            </main>
            <footer>
                <p><a href="index.html">Retour à l'accueil</a></p>
            </footer>
        </body>
        </html>
        """

        # Écrire la page HTML
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Page d'index {page_num} générée : {page_file}")

# Exemple d'utilisation

content_dir = './md'
html_dir = './blog/html'
collections = ['Maroc', 'Indonésie', 'Autre']  # Exemple de collections

generate_index_pages(content_dir, html_dir, collections, articles_per_page=10)
