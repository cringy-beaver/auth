import json

from werkzeug import Response
from flask import request
from ..db import db_handler, User
from ..tokens.token_handler import generate_next_access_token, JWT_UPDATE_THRESHOLD
from .update_token_handler import _update_token

from .app import app


@app.route('/signin', methods=['POST'])
def signin() -> Response:
    login = request.args.get('login')
    password = request.args.get('password')

    if None in [login, password]:
        return Response(json.dumps({
            "error": "invalid_request"
        }), 400)

    user = User(login=login, password=password)

    existed_user = db_handler.authenticate_user_credentials(user)

    if existed_user is None:
        return Response(json.dumps({
            'error': 'access_denied'
        }), 401)

    existed_token = db_handler.get_token_by_owner(existed_user)

    if existed_token is not None:
        response = _update_token(existed_token)
        response_data = json.loads(response.data.decode('utf-8'))

        if response.status_code == 200:
            return Response(
                json.dumps(
                    {
                        'access_token': existed_token,
                        'token_type': 'JWT',
                        'time_create': response_data['time_create'],
                        'ttl': response_data['ttl'],
                        'user': existed_user.to_json()
                    }
                ),
                200
            )

        db_handler.delete_token_owner(existed_token)

    time_create, access_token = generate_next_access_token()
    db_handler.create_new_token_owner(existed_user, access_token)

    return Response(
        json.dumps({
            'access_token': access_token,
            'token_type': 'JWT',
            'time_create': time_create.strftime('%Y-%m-%d %H:%M:%S'),
            'ttl': JWT_UPDATE_THRESHOLD,
            'user': existed_user.to_json()
        }),
        200
    )
