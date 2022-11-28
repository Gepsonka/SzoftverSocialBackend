from datetime import datetime
from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash
from database.database import PostLike, db
from database.database import User, Post, PostMedia
from services.services import get_user_by_username
from database.database import db, Post



post = Blueprint('post', __name__)



@post.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    post_to_get = Post.query.filter_by(id=post_id).one_or_none()

    if post_to_get is None:
        return jsonify({'msg': 'Post not found!'}), 404

    return jsonify(post_to_get.to_dict()), 200



@post.route('/get-personal-posts', methods=['GET'])
@jwt_required()
def get_personal_posts():
    user = get_user_by_username(get_jwt_identity())

    personal_posts = Post.query.filter_by(user_id=user.id).all()

    return jsonify([x.to_dict() for x in personal_posts]), 200




@post.route('/create-post', methods=["POST"])
@jwt_required()
def create_post():
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    req_json = request.get_json()
    user = get_user_by_username(get_jwt_identity())

    if req_json.get('content') == '' or req_json.get('content') is None:
        return jsonify({'msg': 'Content required'}), 400

    new_post = Post(
        title = req_json.get('title'),
        content = req_json.get('content'),
        created_at = datetime.now(),
        updated_at = datetime.now(),
        user_id = user.id
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 200


@post.route('/<post_id>', methods = ['PUT'])
@jwt_required()
def update_post(post_id):
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    req_json = request.get_json()

    post_to_update = Post.query.filter_by(id=post_id).one_or_none()

    if post_to_update is None:
        return jsonify({'msg': 'Post not found!'}), 404

    if post_to_update.user_id != get_user_by_username(get_jwt_identity()).id:
        return jsonify({'msg': 'Cannot update post because it is not yours!'}), 403

    if req_json.get('title') is not None:
        post_to_update.title = req_json.get('title')

    if req_json.get('content') is not None:
        post_to_update.content = req_json.get('content')

    post_to_update.updated_at = datetime.now()

    db.session.commit()

    return jsonify(post_to_update.to_dict())


@post.route('delete-post/<post_id>', methods = ["DELETE"])
@jwt_required()
def delete_post(post_id):
    post_to_delete = Post.query.filter_by(id=post_id).one_or_none()

    if post_to_delete is None:
        return jsonify({'msg': 'Post does not exists!'}), 404

    if post_to_delete.user_id != get_user_by_username(get_jwt_identity()).id:
        return jsonify({'msg': 'Cannot delete post because it is not yours!'}), 403

    db.session.delete(post_to_delete)
    db.session.commit()

    return jsonify(post_to_delete.to_dict()), 200


@post.route('/is-post-liked/<post_id>', methods=['GET'])
@jwt_required()
def is_post_liked(post_id):
    post_to_get = Post.query.filter_by(id=post_id).one_or_none()

    user = get_user_by_username(get_jwt_identity())

    liked = PostLike.query.filter_by(liked_by=user.id, liked_post=post_to_get.id).one_or_none() is not None

    return jsonify({'isLiked': liked}), 200


@post.route('/like-post/<post_id>', methods = ['POST'])
@jwt_required()
def like_post(post_id):
    user = get_user_by_username(get_jwt_identity())

    post_to_like = Post.query.filter_by(id=post_id).one_or_none()

    if post_to_like is None:
        return jsonify({'msg': 'Post not found!'}), 404

    if PostLike.query.filter_by(liked_by = user.id, liked_post = post_to_like.id).one_or_none() is not None:
        return jsonify({'msg': 'Post already liked!'}), 400

    like = PostLike(
        liked_by = user.id,
        liked_post = post_to_like.id
    )

    db.session.add(like)
    db.session.commit()

    return {}, 200


@post.route('/unlike-post/<post_id>', methods=["DELETE"])
@jwt_required()
def unlike_post(post_id):
    user = get_user_by_username(get_jwt_identity())

    post_to_like = Post.query.filter_by(id=post_id).one_or_none()

    like  = PostLike.query.filter_by(liked_by=user.id, liked_post=post_to_like.id).one_or_none()

    if like is None:
        return jsonify({'msg': 'Post is not liked!'}), 404

    if (like is None):
        return 400

    db.session.delete(like)
    db.session.commit()

    return {}, 200

@post.route('/get-liked-post/<post_id>', methods=['GET'])
@jwt_required()
def get_liked_post(post_id):
    liked_post_to_get = Post.query.filter_by(id=post_id).all()

    user = get_user_by_username(get_jwt_identity())

    if liked_post_to_get is None:
        return jsonify({'msg': 'Liked post not found!'}), 404

    if PostLike.query.filter_by(liked_by=user.id, liked_post = liked_post_to_get.id).all() is None:
        return jsonify({'msg': "Post isn't liked!"}), 400

    return jsonify([x.to_dict() for x in liked_post_to_get]), 200