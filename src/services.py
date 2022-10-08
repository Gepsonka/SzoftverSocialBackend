from database.database import User


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).one_or_none()