from xxlimited import new
from flask import Blueprint, request, jsonify
from database.database import User
from constants import ResponseErrorCodes
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user
from services import get_user_by_username

auth = Blueprint('auth', __name__)




@auth.route('/login', methods=['POST'])
def login():
    if request.is_json:
        req_json = request.get_json()
        if not 'username' in req_json or not req_json.get('username'):
            return jsonify({'msg': 'Username required.'})
        
        if not 'password' in req_json or not req_json.get('password'):
            return jsonify({'msg': 'Password required.'})
        
        user = User.query.filter_by(username=req_json.get('username')).one_or_none()
        
        if not user:
            return jsonify({'msg': 'Bad username or password', 'err_code': ResponseErrorCodes.USER_NOT_FOUND.name}), 401
        
        if not check_password_hash(user._password, req_json.get('password')):
            return jsonify({'msg': 'Bad username or password', 'err_code': ResponseErrorCodes.USER_NOT_FOUND.name}), 401
        
        
        access_token = create_access_token(identity=user.username)
        return jsonify({'token': access_token})

    else:
        return jsonify({'msg': 'Not valid json.'}), 400
    
    
@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    new_access_token = create_access_token(identity=get_user_by_username(get_jwt_identity()))
    return jsonify({'refreshedToken': new_access_token}), 201

