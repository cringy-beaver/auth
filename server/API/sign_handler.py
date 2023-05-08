import json

from werkzeug import Response
from flask import redirect, request
from .tools import process_redirect_url
from auth.server.db import db_handler
from auth.server.tokens.token_handler import generate_next_access_token, JWT_UPDATE_THRESHOLD

from .app import app


@app.route('/signin', methods=['POST'])
def signin() -> Response:
    username = request.args.get('username')
    password = request.args.get('password')
    client_id = request.args.get('client_id')
    redirect_url = request.args.get('redirect_url')

    if None in [username, password, client_id, redirect_url]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    if not db_handler.verify_client_info(client_id, redirect_url):
        return Response(json.dumps({
            "error": "invalid_client"
        }), 401)

    if not db_handler.authenticate_user_credentials(username, password):
        return Response(json.dumps({
            'error': 'access_denied'
        }), 401)

    access_token = generate_next_access_token()

    return redirect(process_redirect_url(redirect_url, {
        'access_token': access_token,
        'token_type': 'JWT',
        'time_left': JWT_UPDATE_THRESHOLD
    }), code=303)
