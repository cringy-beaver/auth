from .user import User

token_owner: dict[str, User] = {}


def authenticate_user_credentials(user: User) -> User:
    test_user = User(
        name='John',
        second_name='Doe',
        role='admin',
        _id=1
    )

    return test_user


def verify_new_login(login: str) -> bool:
    return True


def register_new_user(user: User) -> bool:
    return True


def update_token_owner(old_token: str, new_token: str) -> None:
    user = token_owner[old_token]
    del token_owner[old_token]
    token_owner[new_token] = user


def create_new_token_owner(user: User, token: str) -> None:
    token_owner[token] = user


def delete_token_owner(token: str) -> None:
    if token not in token_owner:
        return
    del token_owner[token]


def get_token_owner(token: str) -> User:
    return token_owner[token]
