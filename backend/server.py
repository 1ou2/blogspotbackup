from flask import Flask, request, jsonify, abort
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach  # For sanitizing input
import os
import time
from datetime import datetime

app = Flask(__name__)

# Set up rate limiting (10 requests per IP every minute)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# Function to convert the timestamp into the desired format
def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (id INTEGER PRIMARY KEY, article_id TEXT, username TEXT, content TEXT, timestamp REAL)''')
    conn.commit()
    conn.close()

# Sanitize user input to prevent XSS attacks
def sanitize_input(text):
    return bleach.clean(text)

# Honeypot field - check if the hidden field is filled out (detect bots)
def honeypot_check(data):
    if 'honeypot' in data and data['honeypot']:
        return True  # It's a bot (honeypot was filled out)
    return False

@app.route('/comments/<article_id>', methods=['GET'])
def get_comments(article_id):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('SELECT username, content, timestamp FROM comments WHERE article_id = ? ORDER BY timestamp DESC', (article_id,))
    comments = c.fetchall()
    conn.close()
    # Format the timestamp before returning the response
    formatted_comments = [
        {
            'username': comment[0],
            'content': comment[1],
            'timestamp': format_timestamp(comment[2])
        } for comment in comments
    ]
    return jsonify(formatted_comments)

@app.route('/comment', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to prevent spam attacks
def add_comment():
    data = request.get_json()

    # Honeypot check - if filled, treat as spam
    if honeypot_check(data):
        abort(400, description="Spam detected")

    article_id = sanitize_input(data['article_id'])
    username = sanitize_input(data['username'])
    content = sanitize_input(data['content'])

    # Reject empty or overly long comments
    if not username or not content or len(content) > 1000:
        abort(400, description="Invalid comment")

    # Check for common spam content (this is a simple example, you can expand this list)
    spam_words = ["buy", "cheap", "click here", "free"]
    if any(word in content.lower() for word in spam_words):
        abort(400, description="Spam content detected")

    timestamp = time.time()

    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('INSERT INTO comments (article_id, username, content, timestamp) VALUES (?, ?, ?, ?)', 
              (article_id, username, content, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
