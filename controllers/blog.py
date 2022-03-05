from flask import Blueprint, render_template, request
import requests
from flask_jwt import jwt_required, current_identity

blog = Blueprint('blog', __name__)

api_url = 'https://api.npoint.io/38823c0454884cd19c9c'
data_response = requests.get(api_url)
blogs_data = data_response.json()


@blog.route('/')
def home():
    return render_template('home.html', blogs=blogs_data)


@blog.route('/blog/<int:post_id>')
def get_blog(post_id):
    return render_template('blog.html', blog=blogs_data[post_id - 1])


@blog.route('/blog/compose', methods=['GET', 'POST'])
@jwt_required()
def compose_post():
    if request.method == 'GET':

        access_token = current_identity
        print(access_token)

        return render_template('compose.html')
    # method is POST
    title = request.form['title']
    subtitle = request.form['subtitle']
    body = request.form['body']
    # MUST SAVE THIS IN DB

    return 'DB > COMMIT > SUCCESS'

