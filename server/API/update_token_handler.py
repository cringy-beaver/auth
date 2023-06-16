import json
import datetime

from werkzeug import Response
from flask import request
from ..tokens.token_handler import update_access_token
from ..tokens.token_status_enum import TokenStatusEnum
from ..db import db_handler

from .app import app


@app.route('/update_token', methods=['POST'])
def update_token() -> Response:
    token = request.args.get('token')

    if None in [token]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    return _update_token(token)


def _update_token(token: str) -> Response:
    response, new_token, time_create, ttl = update_access_token(token)

    if response == TokenStatusEnum.NOT_CHANGED:
        return Response(json.dumps({
            "status": "not_changed",
            "token": new_token,
            "time_create": time_create.strftime('%Y-%m-%d %H:%M:%S'),
            "ttl": ttl
        }), 200)
    if response == TokenStatusEnum.UPDATED:
        db_handler.update_token_owner(token, new_token)
        return Response(json.dumps({
            "status": "updated",
            "token": new_token,
            "time_create": time_create.strftime('%Y-%m-%d %H:%M:%S'),
            "ttl": ttl
        }), 200)
    if response == TokenStatusEnum.EXPIRED:
        db_handler.delete_token_owner(token)
        return Response(json.dumps({
            "error": "expired",
        }), 401)
    if response == TokenStatusEnum.FORBIDDEN:
        db_handler.delete_token_owner(token)
        return Response(json.dumps({
            "error": "not_found",
        }), 401)

    db_handler.delete_token_owner(token)
    return Response(json.dumps({
        "error": "server error"
    }), 500)
