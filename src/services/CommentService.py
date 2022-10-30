import datetime
from database.database import User, Post, PostMedia, PostLike, PostComment
from database.database import db


class CommentService:
    @staticmethod
    def get_comment_by_id(comment_id):
        return PostComment.query.filter_by(id=comment_id).one_or_more()

    def create_comment(content, author_id):
        new_comment = PostComment(
            content=content,
            author=author_id,
            created_at=datetime.datetime.utcnow,
            updated_at=datetime.datetime.utcnow,
        )

        db.session.add(new_comment)
        db.session.commit()

    @staticmethod
    def delete_comment(comment_id):
        comment_to_delete = PostComment.query.filter_by(id=comment_id).one_or_none()

        if comment_to_delete is None:
            raise ValueError('Comment does not exists with this id')

        db.session.delete(comment_to_delete)
        db.session.commit()            

    @staticmethod
    def update_comment(comment_id, content):
        comment_to_update = PostComment.query.filter_by(id=comment_id).one_or_none()

        if comment_to_update is None:
            raise ValueError('Comment does not exists with this id')

        comment_to_update.content = content

        db.session.commit()