import json

from werkzeug import Response
from flask import request
from ..db import db_handler, User
from .app import app


def check_password_requirements(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    return True


@app.route('/register', methods=['POST'])
def register() -> Response:
    login = request.args.get('login')
    password = request.args.get('password')
    name = request.args.get('name')
    second_name = request.args.get('second_name')
    role = request.args.get('role')

    if None in [login, password, name, second_name, role]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    if not db_handler.verify_new_login(login):
        return Response(json.dumps({
            "error": "invalid_username"
        }), 405)

    if not check_password_requirements(password):
        return Response(json.dumps({
            "error": "invalid_password"
        }), 405)

    user = User(login=login, password=password, name=name, second_name=second_name, role=role)
    db_handler.register_new_user(user)

    return Response(json.dumps({
        "status": "ok"
    }), 200)
