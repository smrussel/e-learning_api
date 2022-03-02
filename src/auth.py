from src.constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                             HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
                                             HTTP_409_CONFLICT)
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from src.database import User, db
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(name) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(name=name, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'name': name, "email": email
        }

    }), HTTP_201_CREATED


@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'name': user.name,
                    'email': user.email
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.get("/user")
@jwt_required()
@swag_from('./docs/auth/user.yaml')
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'name': user.name,
        'email': user.email
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
@swag_from('./docs/auth/refresh_token.yaml')
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK
