
from flask import Flask, render_template, request, g, jsonify, Response
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.exceptions import abort
from secure_check import authenticate, identity
from controllers.login import login
from controllers.blog import blog
from controllers.contact import contact
from controllers.about import about
app = Flask(__name__)


app.config['SECRET_KEY'] = 'my_secret_key'
jwt = JWT(app, authenticate, identity)
app.register_blueprint(login)
app.register_blueprint(blog)
app.register_blueprint(contact)
app.register_blueprint(about)


@app.errorhandler(401)
def custom_401(error):
    return Response('Missing JWT in header.', 401, {'Authorization': 'header is required'})


@app.before_request
def authorization_handler():
    headers = request.headers
    if 'auth' in request.path:
        print(request.path)
        return
    if 'Authorization' in headers:
        token = headers.get('Authorization')
        print(token)
    else:
        abort(401)


if __name__ == "__main__":
    app.run(debug=True)
