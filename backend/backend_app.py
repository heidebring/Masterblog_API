from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_new_id():
    """Returns a new id, the max id + 1"""

    return max(post["id"] for post in POSTS) + 1


def get_post_by_id(id):
    """Return the post with the given id"""

    post = [post for post in POSTS if post["id"] == id]
    if len(post) > 0:
        return post[0]


def get_filtered_posts(title_search, content_search):
    """
    Gets the filtered posts where the title includes the title_search or
    the content includes the content_search. Both fields are optional
    """

    filtered_posts = []
    for post in POSTS:
        if title_search:
            if title_search in post["title"]:
                filtered_posts.append(post)
        elif content_search:
            if content_search in post["content"]:
                filtered_posts.append(post)
        else:
            filtered_posts.append(post)

    return filtered_posts


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """Returns all posts"""

    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    """
    Add route for adding a new post. Returns a statuscode of 400
    if the title or the content is missing.
    """

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
    return jsonify(new_post), 200


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    """
    Update route for updating the post with the given id. Returns the statuscode
    404 if the post with the given id cannot be found.
    """

    data = request.get_json()
    title = data.get("title", "")
    content = data.get("content", "")

    post = get_post_by_id(id)
    if not post:
        return jsonify({"error": f"Post with id {id} cannot be found"}), 404

    if title:
        post["title"] = title
    if content:
        post["content"] = content

    return jsonify(post), 200


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    """
    Delete route for deleting the post with the given id. Returns the statuscode
    404 if the post with the given id cannot be found.
    """

    post = get_post_by_id(id)
    if not post:
        return jsonify({"error": f"Post with id {id} cannot be found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted sucessfully"}), 200


@app.route("/api/posts/search", methods=["GET"])
def search():
    search_title = request.args.get("title", "")
    search_content = request.args.get("content", "")

    return jsonify(get_filtered_posts(search_title, search_content)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
