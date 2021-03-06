from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('blog', __name__)


def get_post(id):
    post = get_db().execute(
        'SELECT p.id, title, body, created, likes, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post


def get_post_checked_by_author(id, check_author=True):
    post = get_post(id)
    # check_author argument is defined so that the function can be used to get a post without checking the author
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, likes, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    # request.method is GET
    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post_checked_by_author(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    # request.method is GET
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post_checked_by_author(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>')
def read_more_blog(id):
    post = get_post(id)
    return render_template('blog/blog.html', post=post)


# thumbs up button
@bp.route('/<int:id>/like')
@login_required
def like_blog(id):
    db = get_db()
    db.execute(
        'UPDATE post SET likes = likes + 1'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    post = get_post(id)
    return render_template('blog/blog.html', post=post)

# thumbs down button
@bp.route('/<int:id>/dislike')
@login_required
def dislike_blog(id):
    db = get_db()
    db.execute(
        'UPDATE post SET likes = likes - 1'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    post = get_post(id)
    return render_template('blog/blog.html', post=post)


