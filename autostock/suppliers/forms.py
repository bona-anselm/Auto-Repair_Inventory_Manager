from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email



class AddSupplier(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact = StringField('Address', validators=[DataRequired(Length(min=2, max=120))])
    phone_number = StringField('Phone No')
    submit = SubmitField('Add Supplier')