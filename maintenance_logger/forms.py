from maintenance_logger.models import Personnel,Equipment,Service
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class AddPersonnel(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password_confirm', message='Password must match')])
    password_confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign In')
    
    def validate_email(self, email):
        if Personnel.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered')


class LoginPersonnel(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


    

