from datetime import datetime
import os
from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash
from database.database import db
from database.database import User
from services.services import allowed_file, get_user_by_username



user = Blueprint('user', __name__)



@user.route('/user-update', methods=['PUT', 'PATCH'])
@jwt_required()
def user_update():
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    req_json = request.get_json()
    user = get_user_by_username(get_jwt_identity())

    if 'username' in req_json:
        if User.query.filter_by(username=req_json.get('username')).one_or_none() is not None:
            return jsonify({'mgs': 'Username is taken!'}), 400
        user.username = req_json.get('username')

    if 'firstName' in req_json:
        user.first_name = req_json.get('firstName')

    if 'lastName' in req_json:
        user.last_name = req_json.get('lastName')

    if 'email' in req_json:
        if User.query.filter_by(email=req_json.get('email')).one_or_none() is not None:
            return jsonify({'mgs': 'There is already a user registered with this email!'}), 400
        user.email = req_json.get('email')

    if 'password' in req_json:
        if len(req_json.get('password')) > 0 and len(req_json.get('password')) < 8:
            return jsonify({'msg': "Password length must be at least 8 characters"}), 400

        user._password = generate_password_hash(req_json.get('password'), 12).decode('utf-8')
     
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            if file and allowed_file(file.filename):
                file.save(os.path.join('/media', 'profile_pics', f'{user.id}.{file.filename.split(".")[-1]}'))
                user.profile_pic = os.path.join('/media', 'profile_pics', f'{user.id}.{file.filename.split(".")[-1]}')

    user.updated_at = datetime.now()

    db.session.commit()

    return jsonify(user.to_dict()), 200


@user.route('/user-delete', methods=['DELETE'])
@jwt_required()
def user_delete():
    if not request.is_json:
        return jsonify({'msg': 'Request is not valid json!'}), 400

    user = get_user_by_username(get_jwt_identity())

    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': "User was successfully deleted!"}), 200

@user.route('/profile', methods = ['GET'])
@jwt_required()
def get_profile():
    user = get_user_by_username(get_jwt_identity()).to_dict()
    del user['_password']
    return jsonify(user), 200