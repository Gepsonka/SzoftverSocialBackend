from flask import Blueprint, request, jsonify

register = Blueprint('register', __name__)


@register.route('/register', methods=['POST'])
def user_register():
    if request.is_json:
        return jsonify({'msg': 'Json data is not valid'}), 400
    
    else :
        return jsonify({'msg': 'Json data is not valid'}), 400