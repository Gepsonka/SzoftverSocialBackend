import enum


PASSWORD_HASH_ITERATIONS = 12

class ResponseErrorCodes(enum.Enum):
    USER_NOT_FOUND = 'USER_NOT_FOUND'