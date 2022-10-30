from datetime import timedelta
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from database.database import db, User
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from auth import auth
from post import post
from register import register
from services.services import get_user_by_username
from user import user

load_dotenv()

app = Flask(__name__)

print(os.environ.get('SECRET_KEY'))

UPLOAD_FOLDER = '/media'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=8)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PSQL_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MEDIA_SETS'] = 'avatar'

cors = CORS(app, resources={r"/*": {"origins": "*"}})
migrate = Migrate(app, db)
db.init_app(app)
global jwt
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(register)
app.register_blueprint(post, url_prefix='/post')
app.register_blueprint(user)




@app.route('/')
@jwt_required()
def geetings():
    return jsonify({'username': get_user_by_username(get_jwt_identity()).username})



if __name__=='__main__':
    app.run(debug=True)