from flask import Blueprint, render_template, abort, request

login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.route('/login', methods=['GET'])
def render_login():
    return render_template('login.html')


@login_blueprint.route('/login', methods=['POST'])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    return ''

