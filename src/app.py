from turtle import pos
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from database.database import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

from auth import auth
from post import post
from register import register

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
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
def geetings():
    return jsonify({'greeting': "Hi there!"})







if __name__=='__main__':
    app.run(debug=True)