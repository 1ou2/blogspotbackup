import os
import math
import yaml
from datetime import datetime

def generate_index_pages(articles, configuration, collections, articles_per_page=5):
    """Generate index page for the blog"""
    # Pagination
    total_pages = math.ceil(len(articles) / articles_per_page)
    html_dir = configuration['html_dir']
    theme = configuration['theme']
    
    for page_num in range(1, total_pages + 1):
        page_file = os.path.join(html_dir, f'index{"" if page_num == 1 else f"_{page_num}"}.html')
        
        # Generate page content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pigeons voyageurs - Page {page_num}</title>
            <link rel="stylesheet" href="assets/css/index-{theme}.css">
        </head>
        <body>
            <header>
                <h1>Pigeons voyageurs</h1>
                <nav>
                    <ul>
                        <li><a href="index.html">Accueil</a></li>
                        <li><a href="collections/index.html">Collections</a></li>
                    </ul>
                </nav>
            </header>
            <main>
                <section class="article-list">
        """

        # Ajouter les articles de cette page
        start_idx = (page_num - 1) * articles_per_page
        end_idx = start_idx + articles_per_page
        for article in articles[start_idx:end_idx]:
            # articles are 5 levels of directory below
            content = article['html_content'].replace('../../../../../assets','assets')
            html_content += f"""
            <article class="article">
                <h2><a href="{article["link"]}">{article['title']}</a></h2>
                <p class="date">{article['date'].strftime('%d %B %Y').capitalize()}</p>
                <div class="article-meta">
                    <span>Céline et Gabriel</span> | 
                    <time datetime="{article['date'].strftime('%Y-%M-%d').capitalize()}">{article['date'].strftime('%d %B %Y').capitalize()}</time>
                </div>
                <div class="article-content">
                {content}
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
            <footer id="collections">
                <h2>Collections</h2>
                <p>
        """
        for collection in collections:
            html_content += f'<a href="collections/{collection}.html">{collection}</a> '

        html_content += """
                </p>
            </footer>
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
