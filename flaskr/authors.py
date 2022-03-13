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
