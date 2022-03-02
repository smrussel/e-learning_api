from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import db, User
from src.schemas import ma
from flask import Flask, jsonify, abort, request
from src.auth import auth
from src.students import students
from src.courses import course
from src.admins import admin
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.config.swagger import template, swagger_config


jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'xxxxxxxxxxxxxx'
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SWAGGER'] = {
        'title': "Bookmarks API",
        'uiversion': 3
    }
    db.init_app(app)
    ma.init_app(app)

    jwt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(students)

    Swagger(app, config=swagger_config, template=template)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    @app.before_first_request
    def create_table():
        db.create_all()

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
