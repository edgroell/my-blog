import os
import json
from flask import Flask, render_template

app = Flask(__name__)

DATA_PATH = os.path.join("data", "data.json")

def fetch_data():
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {DATA_PATH} was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON.")
        return []

@app.route('/')
def index():
    blog_posts = fetch_data()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
