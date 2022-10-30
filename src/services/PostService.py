import datetime
from database.database import User, Post, PostMedia, PostLike, PostComments
from database.database import db




class PostService:
    @staticmethod
    def get_post(post_id):
        return Post.query.filter_by(id=post_id).one_or_none()

    @staticmethod
    def cerate_post(title:str, content:str, user):
        new_post = Post(
            title=title,
            content=content,
            created_at=datetime.datetime.utcnow,
            updated_at=datetime.datetime.utcnow,
            user_id=user.id
        )

        db.session.add(new_post)
        db.session.commit()

    @staticmethod
    def delete_post(post_id):
        post_to_delete = Post.query.filter_by(id=post_id).one_or_none()

        if post_to_delete is None:
            raise ValueError('Post does not exists with this id')
        
        db.session.delete(post_to_delete)
        db.session.commit()

    @staticmethod
    def update_post(post_id, title='', content=''):
        post_to_update = Post.query.filter_by(id=post_id).one_or_none()

        if post_to_update is None:
            raise ValueError('Post does not exists with this id')
        else:
            post_to_update.title = title
            post_to_update.content = content
            post_to_update.updated_at = datetime.datetime.utcnow

            db.session.commit()

    @staticmethod
    def get_num_of_likes(post_id):
        post_to_get = Post.query.filter_by(id=post_id).one_or_none()

        if post_to_get is None:
            raise ValueError('Post does not exists with this id')

        return PostLike.query.filter_by(post_id=post_to_get.id).count()


    @staticmethod
    def get_post_comments(post_id):
        post_to_get = Post.query.filter_by(id=post_id).one_or_none()

        if post_to_get is None:
            raise ValueError('Post does not exists with this id')

        return PostComments.query.filter_by(post_id=post_to_get.id).order_by(PostComments.updated_at)