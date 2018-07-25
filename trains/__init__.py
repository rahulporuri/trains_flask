import os

from flask import Flask, flash

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

    from . import db

    @app.route('/')
    def home():
        return 'see /trains for general info and /train/* for specific info'

    # a simple page that says hello
    @app.route('/trains')
    def trains():
        database = db.get_db()
        available_trains = database.execute('SELECT trainNumber from trains').fetchall()
        return ', '.join([str(column) for row in available_trains for column in row])

    @app.route('/train/<train_no>')
    def train(train_no):
        database = db.get_db()
        train_info = database.execute(
            'SELECT * FROM trains WHERE trainNumber = ?', (str(train_no), )
        ).fetchall()

        if train_info is None:
            error = 'Data for train number doesnt exist'
            flash(error)

        return ', '.join([str(column) for row in train_info for column in row])


    db.init_app(app)

    return app
