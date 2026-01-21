from flask import Flask
from flask_mysqldb import MySQL
from flask_session import Session

mysql = MySQL()
sess = Session()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    mysql.init_app(app)
    sess.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
