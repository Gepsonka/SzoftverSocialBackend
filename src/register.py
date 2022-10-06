from datetime import datetime
from flask import Blueprint
from flask import jsonify, request
from database.database import User, db
import re
from flask_bcrypt import generate_password_hash

register = Blueprint('register', __name__)

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


@register.route('/register', methods=['POST'])
def user_register():
    if request.is_json:
        req_json = request.get_json()
        print(req_json)
        if not 'firstName' in req_json or not req_json.get('firstName'):
            return jsonify({'mgs': 'Firstname required!'}), 400
        
        if not 'lastName' in req_json or not req_json.get('lastName'):
            return jsonify({'mgs': 'Lastname required!'}), 400
        
        if not 'username' in req_json or not req_json.get('username'):
            return jsonify({'mgs': 'Username required!'}), 400
        
        if User.query.filter_by(username=req_json.get('username')).first():
            return jsonify({'mgs': 'Username is taken!'}), 400
        
        if len(req_json.get('username')) < 8:
            return jsonify({'mgs': 'Username min length is 8!'}), 400
        
        if not 'dateOfBirth' in req_json or not req_json.get('dateOfBirth'):
            return jsonify({'mgs': 'Date of birth required!'}), 400
        
        if not 'email' in req_json or not req_json.get('email'):
            return jsonify({'mgs': 'Email required!'}), 400
        
        if User.query.filter_by(email=req_json.get('email')).first():
            return jsonify({'mgs': 'There is already a user registered with this email!'}), 400
        
        if not re.fullmatch(EMAIL_REGEX, req_json.get('email')):
            return jsonify({'mgs': 'Email is not valid!'}), 400
        
        if not 'password' in req_json or not req_json.get('password'):
            return jsonify({'mgs': 'Password required!'}), 400
        
        if len(req_json.get('password')) < 6:
            return jsonify({'mgs': 'Password length must be longer than 6 characters!'}), 400
        
        if re.search('[0-9]',req_json.get('password')) is None:
            return jsonify({'mgs': 'Password must contain numbers!'}), 400
        
        if re.search('[a-zA-Z]',req_json.get('password')) is None: 
            return jsonify({'mgs': 'Password must contain letters!'}), 400
        
        
        new_user = User(
            username=req_json.get('username'), 
            email=req_json.get('email'),
            first_name=req_json.get('firstName'),
            last_name=req_json.get('lastName'),
            date_of_birth=datetime.strptime(req_json.get('dateOfBirth'), '%m/%d/%Y'),
            updated_at=datetime.now(),
            created_at=datetime.now(),
            _password=generate_password_hash(req_json.get('password'), 12)
        )
            
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'msg': 'User successfully created'}), 201
    
    else :
        return jsonify({'msg': 'Json data is not valid'}), 400