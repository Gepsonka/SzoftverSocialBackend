import enum


PASSWORD_HASH_ITERATIONS = 12

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class ResponseErrorCodes(enum.Enum):
    USER_NOT_FOUND = 'USER_NOT_FOUND'