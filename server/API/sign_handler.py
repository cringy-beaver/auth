import json

from werkzeug import Response
from flask import redirect, request
from .tools import process_redirect_url
from auth.server.db import db_handler, User
from auth.server.tokens.token_handler import generate_next_access_token, JWT_UPDATE_THRESHOLD

from .app import app


@app.route('/signin', methods=['POST'])
def signin() -> Response:
    login = request.args.get('login')
    password = request.args.get('password')
    role = request.args.get('role')

    redirect_url = request.args.get('redirect_url')

    if None in [login, password, role, redirect_url]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    user = User(login=login, password=password, role=role)

    existed_user = db_handler.authenticate_user_credentials(user)

    if existed_user is None:
        return Response(json.dumps({
            'error': 'access_denied'
        }), 401)

    access_token = generate_next_access_token()
    db_handler.create_new_token_owner(existed_user, access_token)

    return redirect(process_redirect_url(redirect_url, {
        'access_token': access_token,
        'token_type': 'JWT',
        'time_left': JWT_UPDATE_THRESHOLD
    }), code=303)
