from flask import Blueprint, render_template
from flaskr.db import get_db

bp = Blueprint('authors', __name__)


@bp.route('/authors')
def authors():
    db = get_db()
    authors = db.execute(
        'SELECT username FROM user',
    ).fetchall()
    return render_template('authors.html', authors=authors)


@bp.route('/authors/<string:username>')
def authors_by_username(username):
    db = get_db()
    posts_by_username = db.execute(
        'SELECT p.id, title, body, created, likes, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE u.username = ?', (username,)
    ).fetchall()
    return render_template('blog/index.html', posts=posts_by_username)
