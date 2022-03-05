from flask import Blueprint, render_template, abort, request

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET'])
def render_login():
    return render_template('login.html')


@login.route('/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    return ''

