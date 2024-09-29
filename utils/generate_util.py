import markdown,yaml
import datetime
import os,shutil
import re


def parse_markdown_article(md_file_path):
    """Parse markdown file, extract meta data and content"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # Use regex to extract the YAML front matter
        yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
        match = yaml_pattern.match(content)

        if match:
            yaml_content = match.group(1)
            md_content = content[match.end():]

            # Parse YAML content
            try:
                meta_data = yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                # If YAML parsing fails, try a custom approach
                # some data contains ':' so we split on the first ':' encountered
                print(f"Error parsing YAML in {md_file_path}: {e}")
                meta_data = {}
                for line in yaml_content.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        meta_data[key.strip()] = value.strip()

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
                img_prefix= os.path.basename(file).replace('.html', '') + '_'
                articles.append({
                    'title': title,
                    'date': date,
                    'tags': tags,
                    'link': article_relative_path,
                    'file_path' : os.path.join(root, file),
                    'img_prefix' : img_prefix,
                    'html_content' : markdown.markdown(md_content)
                })

    
    articles = sorted(articles, key=lambda x: x['date'], reverse=True)
    return articles

def clean_output_directory(output_dir):
    """Clean up the output directory before generating new content."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def clean_and_create_dirs(all_dirs):
    for dir_path in all_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    for dir_path in all_dirs:  
        os.makedirs(dir_path)

def get_image_names(html_content):
    img_pattern =  r'images/[^/]+?\.(?:jpg|jpeg|png|heic)'
    imgs = re.findall(img_pattern, html_content, re.IGNORECASE)
    # remove duplicates in imgs
    return list(set(imgs))