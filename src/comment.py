from datetime import datetime
from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.database import User, Post, PostMedia
from services.services import get_user_by_username
from database.database import db, Post, PostComment, CommentLike

comment = Blueprint('comment', __name__)


@comment.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    post_to_get = PostComment.query.filter_by(id=comment_id).one_or_none()

    if post_to_get is None:
        return jsonify({'msg': 'Comment does not exists'}), 404

    return jsonify(post_to_get.to_dict()), 200


@comment.route('/create-comment', methods=['POST'])
@jwt_required()
def create_comment():
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    req_json = request.get_json()

    user = get_user_by_username(get_jwt_identity())

    if req_json.get('content') == '' or req_json.get('content') is None:
        return jsonify({'msg': 'Content required'}), 400

    comment = PostComment(
        author = user.id,
        content = req_json.get('content'),
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201

@comment.route('delete-comment/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    comment_to_delete = PostComment.query.filter_by(id=comment_id).one_or_none()

    if comment_to_delete is None:
        return jsonify({'msg': 'Comment does not exists'}), 404

    if comment_to_delete.user_id != get_user_by_username(get_jwt_identity()).id:
        return jsonify({'msg': 'Cannot delete comment because it is not yours!'}), 403

    db.session.delete(comment_to_delete)
    db.session.commit()

    return jsonify(comment_to_delete.to_dict()), 200

@comment.route('/<comment_id>', methods = ['PUT'])
@jwt_required()
def update_comment(comment_id):
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    req_json = request.get_json()

    comment_to_update = PostComment.query.filter_by(id=comment_id).one_or_none()

    if comment_to_update is None:
        return jsonify({'msg': 'Comment does not exist!'}), 404

    if comment_to_update.user_id != get_user_by_username(get_jwt_identity()).id:
        return jsonify({'msg': 'Cannot update comment because it is not yours!'}), 403

    if req_json.get('content') is not None:
        comment_to_update.content = req_json.get('content')

    comment_to_update.updated_at = datetime.now()

    db.session.commit()

    return jsonify(comment_to_update.to_dict())

@comment.route('/like-comment/<comment_id>', methods = ['POST'])
@jwt_required()
def like_comment(comment_id):
    user = get_user_by_username(get_jwt_identity())

    comment_to_like = PostComment.query.filter_by(id=comment_id).one_or_none()

    if comment_to_like is None:
        return jsonify({'msg': 'Comment not found!'}), 404

    if PostComment.query.filter_by(liked_by = user.id, liked_comment = comment_to_like.id).one_or_none() is not None:
        return jsonify({'msg': 'Comment is already liked!'}), 400

    like = CommentLike(
        liked_by = user.id,
        liked_post = comment_to_like.id
    )

    db.session.add(like)
    db.session.commit()

    return {}, 200

@comment.route('/unlike-comment/<comment_id>', methods = ['DELETE'])
@jwt_required()
def unlike_comment(comment_id):

    user = get_user_by_username(get_jwt_identity())

    comment_to_like = PostComment.query.filter_by(id=comment_id).one_or_none()

    like  = PostComment.query.filter_by(liked_by=user.id, liked_comment=comment_to_like.id).one_or_none()

    if like is None:
        return jsonify({'msg': 'Comment is not liked!'}), 404

    if (like is None):
        return 400

    db.session.delete(like)
    db.session.commit()

    return {}, 200

@comment.route('/get-liked-comment/<comment_id>', methods = ['GET'])
@jwt_required()
def get_liked_comment(comment_id):
    liked_comment_to_get = PostComment.query.filter_by(id=comment_id).all()

    user = get_user_by_username(get_jwt_identity())

    if liked_comment_to_get is None:
        return jsonify({'msg': 'Liked comment not found!'}), 404

    if CommentLike.query.filter_by(liked_by=user.id, liked_comment=liked_comment_to_get.id).all() is None:
        return jsonify({'msg': "Comment isn't liked!"}), 400

    return jsonify([x.to_dict() for x in liked_comment_to_get]), 200