from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.database import User, Post, PostMedia
from services.services import get_user_by_username
from database.database import db, Post, PostComment

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

