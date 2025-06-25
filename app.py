"""
Program My Blog
by Ed Groell
last on 25-JUN-2025
"""

import os
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_PATH = os.path.join("data", "data.json")


def fetch_data() -> list:
    """ Get the data from the JSON file """
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


def save_data(data: list[dict]) -> None:
    """ Save the data in JSON format """
    with open(DATA_PATH, 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=4)


def generate_unique_id(blog_posts: list[dict]) -> int:
    """ Generate a unique ID for the blog post """
    if not blog_posts:

        return 1

    max_id = max(post["id"] for post in blog_posts)

    return max_id + 1


def fetch_post_by_id(blog_posts: list[dict], post_id: int) -> dict | None:
    """ Get a specific blog post based on given ID """
    for post in blog_posts:
        if post["id"] == post_id:

            return post


@app.route('/add', methods=['GET', 'POST'])
def add():
    """ Add a new blog post """
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        blog_posts = fetch_data()
        new_id = generate_unique_id(blog_posts)
        blog_posts.append({"id": new_id, "title": title, "author": author, "content": content, "likes": 0})

        save_data(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """ Delete a blog post """
    blog_posts = fetch_data()

    updated_blog_posts = [post for post in blog_posts if post.get("id") != post_id]

    save_data(updated_blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """ Edit/Update an existing blog post """
    blog_posts = fetch_data()
    post = fetch_post_by_id(blog_posts, post_id)
    if post is None:

        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_data(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """ Like a blog post - button displays the current amount of likes """
    blog_posts = fetch_data()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1

            break

    save_data(blog_posts)

    return redirect(url_for('index'))


@app.route('/')
def index():
    """ Display all blog posts available in the database """
    blog_posts = fetch_data()

    return render_template('index.html', posts=blog_posts)


@app.errorhandler(404)
def page_not_found(e):
    """ Display a customized 404 page should a page not be found """

    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
