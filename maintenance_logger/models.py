from maintenance_logger import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class Personnel(db.Model, UserMixin):
    __tablename__ = 'personnel'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email= db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    services = db.relationship('Service', backref='personnel', lazy=True)

    def __init__(self,first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email=email
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Equipment(db.Model):
    __tablename__ = 'equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64))
    services = db.relationship('Service', backref='equipment', lazy=True)


class Service(db.Model):
    __tablename__='services'

    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    description = db.Column(db.Text)
