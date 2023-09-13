from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired



class AddInventory(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    supplier = SelectField('Select Supplier', validators=[DataRequired()])
    submit = SubmitField('Add Inventory')