from maintenance_logger.models import Employee,Equipment,Service
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError



class LoginEmployee(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')




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


    

