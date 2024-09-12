import os
import shutil
import markdown
from datetime import datetime
from jinja2 import Template

class Post:
    def __init__(self, title, date, source_path,content, images):
        self.title = title
        self.date = date
        self.source_path = source_path
        self.content = content
        self.images = images
        self.year, self.month, self.day = date.split("-")

def parse_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    md = markdown.Markdown(extensions=['meta'])
    html_content = md.convert(content)
    
    title = md.Meta.get('title', ['Untitled'])[0]

    
    return title, html_content

def get_images(folder_path):
    return [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif',".heic"))]

def generate_website(source_dir, output_dir):
    posts = []
    
    for year in os.listdir(source_dir):
        year_path = os.path.join(source_dir, year)
        if os.path.isdir(year_path):
            for month in os.listdir(year_path):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path):
                    for day in os.listdir(month_path):
                        day_path = os.path.join(month_path, day)
                        for folder in os.listdir(day_path):
                            folder_path = os.path.join(day_path, folder)
                            if os.path.isdir(folder_path):
                                md_file = next((f for f in os.listdir(folder_path) if f.endswith('.md')), None)
                                if md_file:
                                    md_path = os.path.join(folder_path, md_file)
                                    date = f"{year}-{month}-{day}"
                                    title, content = parse_markdown_file(md_path)
                                    images = get_images(folder_path)
                                    posts.append(Post(title, date, folder_path,content, images))

    # Sort posts by date
    #posts.sort(key=lambda x: x.date, reverse=True)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Copy images
    for post in posts:
        src_dir = post.source_path
        dst_dir = os.path.join(output_dir, post.year, post.month, post.day, src_dir.split('/')[-1])
        os.makedirs(dst_dir, exist_ok=True)
        for image in post.images:
            shutil.copy2(os.path.join(src_dir, image), dst_dir)

    # Generate HTML files
    generate_index(output_dir, posts)
    for post in posts:
        generate_post(output_dir, post)

def generate_index(output_dir, posts):
    template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Blog</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <header>
            <h1>My Blog</h1>
        </header>
        <main>
            {% for post in posts %}
            <article>
                <h2><a href="{{ post.date }}/index.html">{{ post.title }}</a></h2>
                <time datetime="{{ post.date }}">{{ post.date }}</time>
            </article>
            {% endfor %}
        </main>
    </body>
    </html>
    ''')
    
    index_html = template.render(posts=posts)
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

def generate_post(output_dir, post):
    template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ post.title }}</title>
        <link rel="stylesheet" href="../style.css">
    </head>
    <body>
        <header>
            <h1>{{ post.title }}</h1>
            <time datetime="{{ post.date }}">{{ post.date }}</time>
        </header>
        <main>
            {{ post.content }}
            {% for image in post.images %}
            <img src="{{ image }}" alt="{{ image }}">
            {% endfor %}
        </main>
        <footer>
            <a href="../index.html">Back to Index</a>
        </footer>
    </body>
    </html>
    ''')
    
    post_html = template.render(post=post)
    post_dir = os.path.join(output_dir, post.date)
    with open(os.path.join(post_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(post_html)

def create_css(output_dir):
    css = '''
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    header {
        border-bottom: 1px solid #ccc;
        margin-bottom: 20px;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    '''
    with open(os.path.join(output_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css)

if __name__ == "__main__":
    source_directory = 'md'
    output_directory = 'html'
    
    generate_website(source_directory, output_directory)
    create_css(output_directory)
    print("Website generated successfully!")