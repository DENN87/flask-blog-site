from flask import Blueprint, render_template, session

from flaskr.db import get_db

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/')
def index():
    db = get_db()
    print(session)
    posts = db.execute(
        'SELECT p.id, title, body, created, likes, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    print(f'Posts: {posts}')
    return render_template('blog/index.html', posts=posts)
