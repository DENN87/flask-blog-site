from flask import Blueprint, render_template, request
from flask_jwt import jwt_required

from controllers.blogpost import get_blogs, get_blog_by_id, create_post

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/')
def home():
    return render_template('home.html', blogs=get_blogs())


@blog_blueprint.route('/blog/<int:post_id>')
def get_blog(post_id):
    return render_template('blog.html', blog=get_blog_by_id(post_id))


@blog_blueprint.route('/blog/compose', methods=['GET'])
@jwt_required()
def compose_get():
    return render_template('compose.html')


@blog_blueprint.route('/blog', methods=['POST'])
@jwt_required()
def post_blog():
    # method is POST
    title = request.form['title']
    subtitle = request.form['subtitle']
    body = request.form['body']
    
    # post_id should be generated depending on the length of the get_blogs().length
    create_post(post_id, title, subtitle, body)
    # MUST SAVE THIS IN DB
    return 'DB > COMMIT > SUCCESS'
