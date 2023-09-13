from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from autostock.models import Mechanics
from flask_login import current_user


class CreateMechanicForm(FlaskForm):
    mechanic = StringField('Mechanic Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    is_superuser = BooleanField('Owner', default=False) 
    submit = SubmitField('Create Mechanic')

    def validate_username(self, username):
        mechanic = Mechanics.query.filter_by(username=username.data).first()
        if mechanic:
            raise ValidationError('Mechanic Already Exists')
            
    def validate_email(self, email):
        mechanic = Mechanics.query.filter_by(email=email.data).first()
        if mechanic:
            raise ValidationError('Email Already Exists')

    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = Mechanics.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken')
    

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Mechanics.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already taken')
            

class UpdateMechanicForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    
class RequestForm(FlaskForm):
    item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    quantity_requested = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit Request')


class OwnerActionForm(FlaskForm):
    action = SelectField('Action', choices=[('approve', 'Approve'), ('reject', 'Reject')], validators=[DataRequired()])
    submit = SubmitField('Submit')