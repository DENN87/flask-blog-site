"""
    // save the json api database
        1. end point(/blog) get list of blogposts
        2. get blog post by id
        3. put blog post
        4. post blog post
        5. delete blog post
            2,3,4,5, return element....
            return json
"""
import json


# Import JSON file, Return the list of all blogs
def load_blogs():
    with open('blogs.json', 'r') as file:
        blogs_data = file.read()
        blogs_obj = json.loads(blogs_data)
    return blogs_obj


# Save BLOGS to JSON file after each CRUD operations
def save_blogs(blogs):
    with open('blogs.json', 'w') as file:
        json.dump(blogs, file)


imported_blogs = load_blogs()  # type list


# 1. Get All blogs
def get_blogs():
    if imported_blogs:
        return imported_blogs
    else:
        print('The Blogs List is EMPTY at the moment.')


# 2. GET BY ID blog post
def get_blog_by_id(post_id):
    for post in imported_blogs:
        if post_id == post['id']:
            return post


# 3. PUT blog post (UPDATE)
def update_blog(post_id, post_title, post_subtitle, post_body):
    post = get_blog_by_id(post_id)  # post type() dict
    if post:  # post found by ID proceed with UPDATE
        if post_title == '':
            print('Error Title can\'t be an empty field.')
        else:
            post.update({'title': post_title})
            post.update({'body': post_body})
            post.update({'subtitle': post_subtitle})
            imported_blogs.pop(post_id - 1)
            imported_blogs.insert(post_id - 1, post)
            print('Successfully updated post.')
            save_blogs(imported_blogs)  # saving to external .json file
            return post
    else:  # post not found by ID return Message
        print('Invalid Post Id, please provide a valid Post Id.')


# 4. POST - add a new blog
def create_post(post_id, post_title, post_subtitle, post_body):
    post = get_blog_by_id(post_id)
    if post:
        # post exists, calling update_blog function
        update_blog(post_id, post_title, post_subtitle, post_body)
        print('Post with Id exists, calling update_blog() function.')
    else:
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
