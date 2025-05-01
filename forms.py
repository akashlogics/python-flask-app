from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class ProductForm(FlaskForm):
    code = StringField('Product Code', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class LocationForm(FlaskForm):
    code = StringField('Location Code', validators=[DataRequired()])
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class MovementForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    from_location_id = SelectField('From Location', coerce=int, validators=[Optional()])
    to_location_id = SelectField('To Location', coerce=int, validators=[Optional()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Record')
