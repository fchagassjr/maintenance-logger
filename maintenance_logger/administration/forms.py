from maintenance_logger.models import Employee,Equipment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class AddEmployee(FlaskForm):
    employeeid = IntegerField('Employee ID', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email(),EqualTo('email_confirm', message='Email must match')])
    email_confirm = StringField('Confirm Email')
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm', message='Password must match')])
    password_confirm = PasswordField('Confirm Password')
    
    def validate_employeeid(self, employeeid):
        if Employee.query.filter_by(employeeid=employeeid.data).first():
            raise ValidationError('Employee ID already registered')

    def validate_email(self, email):
        if Employee.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered')


class EditEmployee(FlaskForm):

    employeeid = HiddenField('Employee ID')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Change Password', validators=[EqualTo('password_confirm', message='Password must match')])
    password_confirm = PasswordField('Confirm New Password')
    
    
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user is not None:
            if not str(user.employeeid) == self.employeeid.data:
                raise ValidationError('Email already registered')
     

class AddEquipment(FlaskForm):
    entity = StringField('Entity', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location')
    
    def validate_entity(self, entity):
        if Equipment.query.filter_by(entity=entity.data).first():
            raise ValidationError('Entity already registered')


class EditEquipment(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location')

