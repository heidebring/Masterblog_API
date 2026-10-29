from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_new_id():
    return max(post["id"] for post in POSTS) + 1


@app.route("/api/posts", methods=["GET"])
def get_posts():
    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json()
    title = data.get("title", "")
    content = data.get("content", "")

    if not title:
        return jsonify({"error": "Title is missing"}), 400
    if not content:
        return jsonify({"error": "Content is missing"}), 400

    new_id = get_new_id()
    new_post = {"id": new_id, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify(new_post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
