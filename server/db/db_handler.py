from .user import User
from . import db_api

from hashlib import sha256
from datetime import datetime

token_to_owner: dict[str, User] = {}
owner_to_token: dict[User, str] = {}


def authenticate_user_credentials(user: User) -> User | None:
    users = db_api.select_all_query_execute(
        {
            'login': user.login,
            'password': user.hash_password
        },
        db_api.storage_auth_name
    )

    if users is None:
        return None

    if len(users) > 1:
        raise Exception('Multiple users with same credentials')

    existing_user = User(**users[0])

    return existing_user


def verify_new_login(login: str) -> bool:
    users = db_api.select_all_query_execute(
        {'login': login},
        db_api.storage_auth_name
    )

    if users is None:
        return True

    return False


def generate_id(user: User) -> str:
    user_str = user.str_to_gen_id()
    new_id = sha256(f'{user_str}{str(datetime.now())}'.encode()).hexdigest()

    json = {
        'id': new_id
    }

    while db_api.select_all_query_execute(json, db_api.storage_auth_name) is not None:
        new_id = sha256(f'{user_str}{str(datetime.now())}'.encode()).hexdigest()
        json['id'] = new_id

    return new_id


def register_new_user(user: User) -> None:
    id = generate_id(user)
    db_api.insert_query_execute(
        {
            'login': user.login,
            'password': user.hash_password,
            'name': user.name,
            'second_name': user.second_name,
            'role': user.role,
            'id': id
        },
        db_api.storage_auth_name
    )


def update_token_owner(old_token: str, new_token: str) -> None:
    user = token_to_owner[old_token]
    del token_to_owner[old_token]
    del owner_to_token[user]
    token_to_owner[new_token] = user
    owner_to_token[user] = new_token


def create_new_token_owner(user: User, token: str) -> None:
    token_to_owner[token] = user
    owner_to_token[user] = token


def delete_token_owner(token: str) -> None:
    if token not in token_to_owner:
        return
    user = token_to_owner[token]
    del token_to_owner[token]
    del owner_to_token[user]


def get_token_owner(token: str) -> User:
    return token_to_owner[token]


def get_token_by_owner(user: User) -> str | None:
    if user not in owner_to_token:
        return None

    return owner_to_token[user]
