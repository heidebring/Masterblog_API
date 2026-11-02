from flask import Flask, jsonify, request
from flask_cors import CORS
from helper import (
    get_new_id,
    get_post_by_id,
    get_filtered_posts,
    get_sorted_posts,
)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """
    Returns all posts. Optional query parameters are sort and direction together.
    Sort only accepts the values title and content for sorting the posts according
    to the title or the content. Direction only accepts asc for ascending or desc
    for descending. The use of onvalid sort fields or direction returns a statuscode 400.
    """

    sort = request.args.get("sort", "")
    direction = request.args.get("direction", "")

    if (sort and not direction) or (not sort and direction):
        return (
            jsonify(
                {"error": "Query parameter sort and direction must be used together"}
            ),
            400,
        )

    if sort and not sort in ["title", "content"]:
        return (
            jsonify({"error": "Sort only supports the fields title and content"}),
            400,
        )

    if direction and not direction in ["asc", "desc"]:
        return (
            jsonify({"error": "Direction only supports the orders acs and desc"}),
            400,
        )

    if sort and direction:
        return jsonify(get_sorted_posts(sort, direction, POSTS)), 200

    return jsonify(POSTS), 200


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

    new_id = get_new_id(POSTS)
    new_post = {"id": new_id, "title": title, "content": content}
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    """
    Update route for updating the post with the given id. Returns the statuscode
    404 if the post with the given id cannot be found.
    """

    data = request.get_json()
    title = data.get("title", "")
    content = data.get("content", "")

    post = get_post_by_id(id, POSTS)
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

    post = get_post_by_id(id, POSTS)
    if not post:
        return jsonify({"error": f"Post with id {id} cannot be found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted sucessfully"}), 200


@app.route("/api/posts/search", methods=["GET"])
def search():
    """
    Route for searching the title or the content
    """

    search_title = request.args.get("title", "")
    search_content = request.args.get("content", "")

    return jsonify(get_filtered_posts(search_title, search_content, POSTS)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
