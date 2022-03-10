import json

from flask import Blueprint, request

blog_post_blueprint = Blueprint('blogpost', __name__)


# Import JSON file, Return the list of all blogs
def load_blogs():
    with open('static/blogs.json', 'r') as file:
        blogs_data = file.read()
        blogs_obj = json.loads(blogs_data)
    # type(blogs_obj) - list
    blogs_dict = {b['id']: b for b in blogs_obj}
    # type(blogs_dict) - dict
    return blogs_dict


# Save BLOGS to JSON file after each CRUD operations
def save_blogs(blogs):
    with open('static/blogs.json', 'w') as file:
        json.dump(blogs, file)


imported_blogs = load_blogs()


# return JSON Object

# 1. Get All blogs
@blog_post_blueprint.route('/blogposts')
def get_blogs():
    if imported_blogs:
        # list_blogs = list(imported_blogs.items())
        return imported_blogs  # Returning a dict
    else:
        print('The Blogs List is EMPTY at the moment.')


# 2. GET BY ID blog post
@blog_post_blueprint.route('/blogposts/<int:post_id>', methods=['GET'])
def get_blog_by_id(post_id):
    blog_id = imported_blogs.get(post_id)
    return json.dumps(blog_id)  # Returning JSON str


# 3. PUT blog post (UPDATE)
@blog_post_blueprint.route('/blogposts/<int:post_id>', methods=['PUT'])
def update_blog(post_id):
    post = imported_blogs.get(post_id)  # dict
    # must include Content-type : application/json
    data = request.get_json(force=True)  # force=True will ignore Content-type: app/json
    print(type(data))
    v = data.get('title')

    return data

    # if post:  # post found by ID proceed with UPDATE
    #     post.update({'title': post['title']})
    #     post.update({'body': post['body']})
    #     post.update({'subtitle': post['subtitle']})
    #
    #     imported_blogs.pop(post_id - 1)
    #     imported_blogs.insert(post_id - 1, post)
    #     print('Successfully updated post.')
    #     save_blogs(imported_blogs)  # saving to external .json file
    #     return post
    # else:  # post not found by ID return Message
    #     print('Invalid Post Id, please provide a valid Post Id.')
    #


# 4. POST - add a new blog
@blog_post_blueprint.route('/blogposts', methods=['POST'])
def create_post():
    new_post = {
        'id': post_id,
        'title': post_title,
        'subtitle': post_subtitle,
        'body': post_body
    }
    imported_blogs.append(new_post)
    save_blogs(imported_blogs)  # saving to external .json file
    print('New post created.')
    return new_post


# 5. DELETE - remove post from blogs
@blog_post_blueprint.route('/blogposts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = get_blog_by_id(post_id)
    if post:
        imported_blogs.pop(post_id - 1)
        save_blogs(imported_blogs)  # saving to external .json file
        print('Post deleted successful.')
        return post
    else:
        print(f'No post found by this Id {post_id}.')

# Manual Test Cases
# print(update_blog(1, 'New Title 1', '', 'New body 1'))
# print(create_post(2, 'Title 2', '', 'Body 2'))
# delete_post(2)
# print(imported_blogs)
# print(f'Get imported_blogs type of -> {type(imported_blogs)}')
# print(f'get_blogs() type of -> {type(get_blogs())}')
# print(f'get_blog_by_id() type of -> {type(get_blog_by_id(1))}')
# update_blog(1)
