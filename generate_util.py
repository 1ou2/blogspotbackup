import markdown,yaml
import datetime
import os,shutil

def parse_markdown_article(md_file_path):
    """Parse le fichier markdown pour extraire les métadonnées et le contenu."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        # Lire le contenu brut du fichier markdown
        content = f.read()

        # Séparer l'en-tête YAML du contenu markdown
        if content.startswith('---'):
            _, meta_data, md_content = content.split('---', 2)
            meta_data = yaml.safe_load(meta_data)
        else:
            meta_data = {}
            md_content = content

        return meta_data, md_content

def parse_markdown_metadata(md_file_path):
    """Récupère les métadonnées d'un fichier markdown."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            _, meta_data, _ = content.split('---', 2)
            meta_data = yaml.safe_load(meta_data)
            return meta_data
    return {}

def get_sorted_articles(content_dir):
    articles = []
    # Parcourir les articles et extraire les métadonnées
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                #meta_data = parse_markdown_metadata(md_file_path)
                meta_data, md_content = parse_markdown_article(md_file_path)
                title = meta_data.get('title', 'Sans titre')
                tags = meta_data.get('tags', [])
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
                hour = 23 - int(folder[:2])
                # last 3 elements are the date
                date = datetime.datetime.strptime('/'.join(current_path[-3:]) + f":{hour}", '%Y/%m/%d:%H')

                articles.append({
                    'title': title,
                    'date': date,
                    'tags': tags,
                    'link': article_relative_path,
                    'file_path' : os.path.join(root, file),
                    'html_content' : markdown.markdown(md_content)
                })

    
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)
    return articles

def clean_output_directory(output_dir):
    """Clean up the output directory before generating new content."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)