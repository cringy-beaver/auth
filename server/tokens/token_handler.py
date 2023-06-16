import jwt
import time
import datetime

from .token_status_enum import TokenStatusEnum

ISSUER = 'godoV_Ztepan'
PRIVATE_KEY_PATH = 'server/tokens/keys/private.pem'  # Прикрутить папку с ключами к проекту
PUBLIC_KEY_PATH = 'server/tokens/keys/public.pem'  # Прикрутить папку с ключами к проекту
JWT_LIFE_SPAN = 60 * 60  # 1 hour
JWT_UPDATE_THRESHOLD = JWT_LIFE_SPAN // 2  # 30 minutes

TOKENS_CREATE_TIME: dict[str, datetime.datetime] = {}

with open(PRIVATE_KEY_PATH, 'rb') as f:
    private_key = f.read()

with open(PUBLIC_KEY_PATH, 'rb') as f:
    public_key = f.read()


def generate_next_access_token() -> tuple[datetime.datetime, str]:
    time_created = datetime.datetime.now()
    payload = {
        "iss": ISSUER,
        "ttl": JWT_UPDATE_THRESHOLD,
        'created': time_created.strftime('%Y-%m-%d %H:%M:%S'),
    }

    access_token = jwt.encode(payload, private_key, algorithm='RS256')

    TOKENS_CREATE_TIME[access_token] = time_created
    return time_created, access_token


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


def update_access_token(access_token) -> tuple[TokenStatusEnum, str, datetime.datetime, float]:
    if access_token not in TOKENS_CREATE_TIME:
        return TokenStatusEnum.FORBIDDEN, '', datetime.datetime.now(), 0

    time_passed = (datetime.datetime.now() - TOKENS_CREATE_TIME[access_token]).seconds

    if time_passed > JWT_LIFE_SPAN:
        return TokenStatusEnum.EXPIRED, '', datetime.datetime.now(), 0

    if time_passed >= JWT_UPDATE_THRESHOLD:
        TOKENS_CREATE_TIME[access_token] = datetime.datetime.now()
        del TOKENS_CREATE_TIME[access_token]
        return TokenStatusEnum.UPDATED, generate_next_access_token(), TOKENS_CREATE_TIME[access_token], JWT_UPDATE_THRESHOLD

    return TokenStatusEnum.NOT_CHANGED, access_token, TOKENS_CREATE_TIME[access_token], JWT_UPDATE_THRESHOLD - time_passed + 1
