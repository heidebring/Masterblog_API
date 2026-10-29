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


def get_post_by_id(id):
    post = [post for post in POSTS if post["id"] == id]
    if len(post) > 0:
        return post[0]


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


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = get_post_by_id(id)
    if not post:
        return jsonify({"error": f"Post with id {id} cannot be found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted sucessfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
