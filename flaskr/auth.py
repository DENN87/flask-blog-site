import functools

from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import get_db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


# At the beginning of each request, if a user is logged in their
# information should be loaded and made available to other views
@auth_blueprint.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # Validate that username and password are not empty
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # insert the new user data into the database
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            # if user exists in DB, db.IntegrityError will throw validation error
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        # If validation fails, the error is shown to the user.
        # flash() stores messages that can be retrieved when rendering the template
        flash(error)

    # otherwise, request.method == 'GET'
    return render_template('auth/register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()
        print(f'Logged In user: {user["username"]}')

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stores data across requests. When validation succeeds,
            # the user’s id is stored in a new session. The data is stored in a cookie
            # that is sent to the browser, and the browser then sends it back with
            # subsequent requests. Flask securely signs the data so that it can’t be tampered with.
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index', user=user["username"]))

        # If validation fails, the error is shown to the user.
        # flash() stores messages that can be retrieved when rendering the template
        flash(error)

    # otherwise, request.method == 'GET'
    return render_template('auth/login.html')


# To log out, simply remove the user id from the session and redirect
@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# a decorator function to check each view that a user is logged in,
# in order to create,edit and delete blog posts
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        # If a user is loaded the original view is called and continues
        return view(**kwargs)

    return wrapped_view
