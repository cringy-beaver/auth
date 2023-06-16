import json

from werkzeug import Response
from flask import request
from ..db import db_handler
from .update_token_handler import _update_token

from .app import app


@app.route('/user_info', methods=['GET'])
def get_user_info() -> Response:
    token = request.args.get('token')

    if None in [token]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    response = _update_token(token)

    if response.status_code != 200:
        return response

    user = db_handler.get_token_owner(token)

    if user is None:
        return Response(json.dumps({
            "error": "server error"
        }), 500)

    update_response = json.loads(response.get_data())

    return Response(json.dumps({
        "status": "ok",
        "user": user.to_json(),
        "token_status": update_response["status"],
        "token": update_response["token"],
        "time_create": update_response["time_create"],
        "ttl": update_response["ttl"],
    }), 200)
