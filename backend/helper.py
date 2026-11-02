def get_new_id(posts):
    """Returns a new id, the max id + 1"""

    return max((post["id"] for post in posts), default=0) + 1


def get_post_by_id(id, posts):
    """Return the post with the given id"""

    post = [post for post in posts if post["id"] == id]
    if len(post) > 0:
        return post[0]


def get_filtered_posts(title_search, content_search, posts):
    """
    Gets the filtered posts where the title includes the title_search or
    the content includes the content_search. Both fields are optional.
    """

    filtered_posts = []
    for post in posts:
        if title_search:
            if title_search in post["title"]:
                filtered_posts.append(post)
        if content_search:
            if content_search in post["content"]:
                filtered_posts.append(post)
        else:
            filtered_posts.append(post)

    return filtered_posts


def get_sorted_posts(sort, direction, posts):
    """
    Sorts the posts according to sort and direction and returns them.
    """

    sorted_posts = sorted(
        posts, key=lambda post: post[sort], reverse=(direction == "desc")
    )
    return sorted_posts
