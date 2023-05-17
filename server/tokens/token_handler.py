import jwt
import time

from .token_status_enum import TokenStatusEnum

ISSUER = 'godoV_Ztepan'
PRIVATE_KEY_PATH = 'tokens/keys/private.pem'  # Прикрутить папку с ключами к проекту
PUBLIC_KEY_PATH = 'tokens/keys/public.pem'  # Прикрутить папку с ключами к проекту
JWT_LIFE_SPAN = 60 * 60  # 1 hour
JWT_UPDATE_THRESHOLD = JWT_LIFE_SPAN // 2  # 30 minutes

TOKENS_DEADLINE: dict[str, float] = {}

with open(PRIVATE_KEY_PATH, 'rb') as f:
    private_key = f.read()

with open(PUBLIC_KEY_PATH, 'rb') as f:
    public_key = f.read()


def generate_next_access_token() -> str:
    payload = {
        "iss": ISSUER,
        "exp": time.time() + JWT_UPDATE_THRESHOLD
    }

    access_token = jwt.encode(payload, private_key, algorithm='RS256')

    TOKENS_DEADLINE[access_token] = payload['exp'] - JWT_UPDATE_THRESHOLD
    return access_token


def verify_access_token(access_token) -> TokenStatusEnum:
    try:
        decoded_token = jwt.decode(access_token.encode(), public_key,
                                   issuer=ISSUER,
                                   algorithms=['RS256'])
    except (jwt.exceptions.InvalidTokenError,
            jwt.exceptions.InvalidSignatureError,
            jwt.exceptions.InvalidIssuerError,
            jwt.exceptions.ExpiredSignatureError) as e:
        return TokenStatusEnum.INVALID

    return TokenStatusEnum.SUCCESS


def update_access_token(access_token) -> tuple[TokenStatusEnum, str, float]:
    if access_token not in TOKENS_DEADLINE:
        return TokenStatusEnum.FORBIDDEN, '', 0

    time_passed = time.time() - TOKENS_DEADLINE[access_token]

    if time_passed > JWT_LIFE_SPAN:
        return TokenStatusEnum.EXPIRED, '', 0

    if time_passed >= JWT_UPDATE_THRESHOLD:
        TOKENS_DEADLINE[access_token] = time.time() + JWT_LIFE_SPAN
        del TOKENS_DEADLINE[access_token]
        return TokenStatusEnum.UPDATED, generate_next_access_token(), JWT_UPDATE_THRESHOLD

    return TokenStatusEnum.NOT_CHANGED, access_token, JWT_UPDATE_THRESHOLD - time_passed
