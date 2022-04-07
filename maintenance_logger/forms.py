from xmlrpc.client import DateTime
from maintenance_logger.models import Employee,Equipment,Service
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class AddEmployee(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm', message='Password must match')])
    password_confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign In')
    
    def validate_employee_id(self, employee_id):
        if Employee.query.filter_by(employee_id=employee_id.data).first():
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
    date = DateTimeField('Date', validators=[DataRequired()])
    submit = SubmitField('Create Service Entry')
    
    def validate_entity(self, entity):
        if Equipment.query.filter_by(entity=entity.data).first() is None:
            raise ValidationError('Equipment entity not found')


    

