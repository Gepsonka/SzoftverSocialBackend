from crypt import methods
import os
from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash
from database.database import db
from database.database import User, Post, PostMedia
from services.services import get_user_by_username


post = Blueprint('post', __name__)



@post.route('/create-post', methods=["POST"])
@jwt_required()
def create_post():
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    req_json = request.get_json()
    user = get_user_by_username(get_jwt_identity())

