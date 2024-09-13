import os
import math
import yaml
from datetime import datetime
from generate_util import get_sorted_articles


def generate_index_pages(content_dir, html_dir, collections, articles_per_page=5):
    """Génère la page d'index du blog avec affichage direct des articles."""
    # Créer le répertoire html s'il n'existe pas encore
    os.makedirs(html_dir, exist_ok=True)

    articles = get_sorted_articles(content_dir)

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
                <section class="articles">
        """

        # Ajouter les articles de cette page
        start_idx = (page_num - 1) * articles_per_page
        end_idx = start_idx + articles_per_page
        for article in articles[start_idx:end_idx]:
            html_content += f"""
            <article class="article">
                <h2><a href="{article["link"]}">{article['title']}</a></h2>
                <p class="date">{article['date'].strftime('%d %B %Y')}</p>
                <div class="content">
                    <p>{article['content']}</p>
                </div>
            </article>
            """

        html_content += """
                </section>
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
content_dir = '/chemin/vers/content'
html_dir = '/chemin/vers/html'
collections = ['Maroc', 'Indonésie', 'Autre']  # Exemple de collections

generate_index_pages(content_dir, html_dir, collections, articles_per_page=5)
