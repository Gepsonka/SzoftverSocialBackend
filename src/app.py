from datetime import timedelta
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from database.database import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from auth import auth
from register import register
from post import post

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PSQL_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

migrate = Migrate(app, db)
db.init_app(app)
global jwt
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(register)
app.register_blueprint(post, url_prefix='/post')

@app.route('/')
@jwt_required()
def geetings():
    curr_user = get_jwt_identity()
    return jsonify({'currentUser': curr_user})



if __name__=='__main__':
    app.run(debug=True)