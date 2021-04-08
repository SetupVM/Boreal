from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField, HiddenField
from wtforms.validators import Required
import decimal

CHOICES = (('222', 'Tricoline (97% Algodão e 3% Elastano) - 195 g/m'), ('221', 'Viscose (100% Viscose) - 160 g/m'))

class CartForm(FlaskForm):
    image = HiddenField()
    tecido = SelectField(choices=CHOICES)
    quantity = DecimalField(places=1, rounding=decimal.ROUND_UP)
    submit = SubmitField()