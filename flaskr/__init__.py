import os

from flask import Flask

from flaskr import db, auth, about, contact, blogpost


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello Flask world !'

    # registering DB with app
    db.init_app(app)

    # registering Blueprints
    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(about.about_blueprint)
    app.register_blueprint(contact.contact_blueprint)
    app.register_blueprint(blogpost.blogpost_blueprint)
    app.add_url_rule('/', endpoint='index')

    return app