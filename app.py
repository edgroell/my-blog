import os
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_PATH = os.path.join("data", "data.json")


def fetch_data():
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as handle:
            data = json.load(handle)

        return data

    except FileNotFoundError:
        print(f"Error: The file at {DATA_PATH} was not found.")

        return []

    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON.")

        return []


def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=4)


def generate_unique_id(blog_posts):
    if not blog_posts:
        return 1
    max_id = max(post["id"] for post in blog_posts)

    return max_id + 1


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        blog_posts = fetch_data()
        new_id = generate_unique_id(blog_posts)
        blog_posts.append({"id": new_id, "title": title, "author": author, "content": content})

        save_data(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/')
def index():
    blog_posts = fetch_data()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
