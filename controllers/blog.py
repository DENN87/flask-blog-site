from flask import Blueprint, render_template, request
import requests
from flask_jwt import jwt_required, current_identity

blog_blueprint = Blueprint('blog', __name__)


def get_blogs_data():
    api_url = 'https://api.npoint.io/38823c0454884cd19c9c'
    data_response = requests.get(api_url)
    blogs_data = data_response.json()
    return blogs_data


@blog_blueprint.route('/')
def home():
    return render_template('home.html', blogs=get_blogs_data())


@blog_blueprint.route('/blog/<int:post_id>')
def get_blog(post_id):
    return render_template('blog.html', blog=get_blogs_data()[post_id - 1])


@blog_blueprint.route('/blog', methods=['POST'])
@jwt_required()
def post_blog():
    # method is POST
    title = request.form['title']
    subtitle = request.form['subtitle']
    body = request.form['body']
    # MUST SAVE THIS IN DB
    return 'DB > COMMIT > SUCCESS'


@blog_blueprint.route('/blog/compose', methods=['GET'])
@jwt_required()
def compose_get():
    return render_template('compose.html')


