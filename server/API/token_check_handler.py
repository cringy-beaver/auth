import json

from werkzeug import Response
from flask import request
from auth.server.tokens.token_handler import update_access_token
from auth.server.tokens.token_status_enum import TokenStatusEnum

from .app import app


@app.route('/update_token', methods=['POST'])
def update_token() -> Response:
    token = request.args.get('token')

    if None in [token]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    response, new_token, time_left = update_access_token(token)

    if response == TokenStatusEnum.NOT_CHANGED:
        return Response(json.dumps({
            "status": "not_changed",
            "token": new_token,
            "time_left": time_left
        }), 200)
    if response == TokenStatusEnum.UPDATED:
        return Response(json.dumps({
            "status": "updated",
            "token": new_token,
            "time_left": time_left
        }), 200)
    if response == TokenStatusEnum.EXPIRED:
        return Response(json.dumps({
            "status": "expired",
        }), 401)
    if response == TokenStatusEnum.FORBIDDEN:
        return Response(json.dumps({
            "status": "not_found",
        }), 401)

    return Response(json.dumps({
        "status": "error"
    }), 500)
