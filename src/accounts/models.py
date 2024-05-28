from src import bcrypt,db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    created_on = db.Column(db.DateTime,nullable=False)
    is_admin = db.Column(db.Boolean,default=False,nullable=False)

    def __init__(self,email,password,is_admin=False):
        self.email = email,
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return self.email