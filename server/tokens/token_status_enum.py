import enum


class TokenStatusEnum(enum.Enum):
    FORBIDDEN = 0
    SUCCESS = 1
    EXPIRED = 2
    INVALID = 3
    UPDATED = 4
    NOT_CHANGED = 5