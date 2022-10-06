from urllib import request
from flask import Blueprint
from flask import jsonify

register = Blueprint('register', __name__)


@register.route('/register', methods=['POST'])
def register():
    if request.is_json():
        pass
    
    else :
        return jsonify({'msg': 'Json data is not valid'}), 400