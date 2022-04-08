from maintenance_logger import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employeeid = db.Column(db.Integer, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email= db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    services = db.relationship('Service', backref='employee', lazy=True)

    def __init__(self,employeeid,firstname,lastname,email,password):
        self.employeeid = employeeid
        self.firstname = firstname
        self.lastname = lastname
        self.email=email
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"


class Equipment(db.Model):
    __tablename__ = 'equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64))
    location = db.Column(db.String(64))
    services = db.relationship('Service', backref='equipment', lazy=True)

    def __init__(self,entity,description,location):
        self.entity=entity
        self.description=description
        self.location=location


class Service(db.Model):
    __tablename__='services'

    id = db.Column(db.Integer, primary_key=True)
    employeeid = db.Column(db.Integer, db.ForeignKey('employees.id'))
    equipmentid = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    description = db.Column(db.Text)
    servdate = db.Column(db.Date)
    def __init__(self, employeeid, equipmentid,description, servdate):
        self.employeeid = employeeid
        self.equipmentid = equipmentid
        self.description = description
        self.servdate = servdate
