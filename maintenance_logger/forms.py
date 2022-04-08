from maintenance_logger.models import Employee,Equipment,Service
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class AddEmployee(FlaskForm):
    employeeid = IntegerField('Employee ID', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm', message='Password must match')])
    password_confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign In')
    
    def validate_employeeid(self, employeeid):
        if Employee.query.filter_by(employeeid=employeeid.data).first():
            raise ValidationError('Employee ID already registered')

    def validate_email(self, email):
        if Employee.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered')


class LoginEmployee(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AddEquipment(FlaskForm):
    entity = StringField('Entity', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location')
    submit = SubmitField('Add Equipment')
    
    def validate_entity(self, entity):
        if Equipment.query.filter_by(entity=entity.data).first():
            raise ValidationError('Entity already registered')


class AddService(FlaskForm):
    entity = StringField('Equipment Entity', validators=[DataRequired()])
    description = StringField('Service Description', validators=[DataRequired()])
    servdate = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Create Service Entry')
    
    def validate_entity(self, entity):
        if Equipment.query.filter_by(entity=entity.data).first() is None:
            raise ValidationError('Equipment entity not found')

    def validate_servdate(self, servdate):
        if servdate.data > date.today():
            raise ValidationError('Date cannot be in the future')


    

