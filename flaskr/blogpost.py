import json

from flask import Blueprint, request

blog_post_blueprint = Blueprint("blogpost", __name__)


# Import JSON file, Return the list of all blogs
def load_blogs():
    with open("static/blogs.json", 'r') as file:
        blogs_data = file.read()
        blogs_obj = json.loads(blogs_data)  # type list
    blogs_dict = {b["id"]: b for b in blogs_obj}  # type dict
    return blogs_dict


imported_blogs = load_blogs()


# 1. Get All blogs
@blog_post_blueprint.route("/blogposts")
def get_blogs():
    if imported_blogs:
        return json.dumps(imported_blogs)  # Returning JSON str
    else:
        print("The Blogs List is EMPTY at the moment.")


# 2. GET BY ID blog post
@blog_post_blueprint.route("/blogposts/<int:post_id>", methods=["GET"])
def get_blog_by_id(post_id):
    blog_id = imported_blogs.get(post_id)
    return json.dumps(blog_id)  # Returning JSON str


# 3. PUT blog post (UPDATE)
@blog_post_blueprint.route("/blogposts/<int:post_id>", methods=["PUT"])
def update_blog(post_id):
    # must include Content-type : application/json
    # force=True will ignore Content-type: app/json
    data = request.get_json(force=True)
    imported_blogs[post_id].update(data)
    print("Successfully updated blog requested.")
    return json.dumps(imported_blogs[post_id])  # Returning JSON str


# 4. POST - add a new blog
@blog_post_blueprint.route("/blogposts", methods=["POST"])
def create_post():
    data = request.get_json(force=True)
    int_id = int(data["id"])
    imported_blogs[int_id] = data
    print("New post successfully created.")
    return json.dumps(imported_blogs[int_id])  # Returning JSON str


# 5. DELETE - remove post from blogs
@blog_post_blueprint.route("/blogposts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    to_delete = imported_blogs.get(post_id)
    imported_blogs.pop(post_id)
    print("Post deleted successful.")
    return json.dumps(to_delete)  # Returning JSON str
