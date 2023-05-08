import json

from werkzeug import Response
from flask import redirect, request
from auth.server.db import db_handler
from .tools import process_redirect_url
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
    username = request.args.get('username')
    password = request.args.get('password')
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')

    if None in [username, password, client_id, redirect_url]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    if not db_handler.verify_new_login(username):
        return Response(json.dumps({
            "error": "invalid_username"
        }), 405)

    if not check_password_requirements(password):
        return Response(json.dumps({
            "error": "invalid_password"
        }), 405)

    db_handler.register_new_user(username, password)

    # redirect to signin
    return redirect(process_redirect_url(redirect_url, {
        'client_id': client_id,
        'redirect_url': redirect_url
    }), code=303)
