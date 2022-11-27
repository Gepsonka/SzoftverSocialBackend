import datetime
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import generate_password_hash
from sqlalchemy_serializer import SerializerMixin


BCRYPT_LOG_ROUNDS = 12


db = SQLAlchemy()

 
class User(db.Model, SerializerMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.DateTime)
    profile_pic = db.Column(db.String, )
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    _password = db.Column(db.String(128), unique=True, nullable=False)
    
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def _set_password(self, text):
        self._password = generate_password_hash(text, BCRYPT_LOG_ROUNDS)



class Post(db.Model, SerializerMixin):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(127))
    content = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user_rel = db.relation('User')
    
    
class PostLike(db.Model, SerializerMixin):
    __tablename__ = "PostLikes"
    id = db.Column(db.Integer, primary_key=True)
    liked_by = db.Column(db.Integer, db.ForeignKey('User.id'))
    liked_post = db.Column(db.Integer, db.ForeignKey('Post.id'))
    liked_by_rel = db.relation('User')
    liked_post_rel = db.relation('User')
    
    __table_args__ = (
        db.UniqueConstraint('liked_by', 'liked_post', name='unique_component_commit'),
    )
    
class PostComment(db.Model, SerializerMixin):
    __tablename__ = "PostComment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey('User.id'))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author_rel = db.relation('User')


class PostMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.String, unique=True)
    post = db.Column(db.Integer, db.ForeignKey('User.id'))
    post_rel = db.relation('User')
