#imports from SQLAlchemy - ORM
from flask_sqlalchemy import SQLAlchemy

#flask_migrate imports
from flask_migrate import Migrate

import uuid

#timestamp for user creation
from datetime import datetime

#add flask security for hashing passwords
from werkzeug.security import generate_password_hash, check_password_hash

#create a user token
import secrets

#imports from flask login
from flask_login import UserMixin, LoginManager


#imports from flask-marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_nmae = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    marvel = db.relationship('Marvel', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_nmae = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"

class Marvel(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Integer, nullable = True)
    super_power = db.Column(db.String(100), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token

    def __repr__(self):
        return f"The following Marvel has been added: {self.name}"

    def set_id(self):
        return secrets.token_urlsafe()

class MarvelSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power' ]

marvel_schema = MarvelSchema()
marvels_schema = MarvelSchema(many = True)



