import os

from flask import Flask

TRAIN_LIST = ['12466', '18844', '12345']


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'trains.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        return 'see /trains for general info and /train/* for specific info'

    # a simple page that says hello
    @app.route('/trains')
    def trains():
        render_str = "Information about the following trains is available"
        return render_str + f"{', '.join(TRAIN_LIST)}"

    @app.route('/train/<train_no>')
    def train(train_no):
        print(train_no)
        return f"{train_no}"

    return app
