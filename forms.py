from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,ValidationError
from models import Users

class LoginForm(FlaskForm):
    name = StringField('Name')
    password = PasswordField('Password')
    # submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    name = StringField('Name')
    password = PasswordField('Password')
    # submit = SubmitField('Sign up')

    def validate_name(self, name):
        if Users.query.filter_by(name=name.data).one_or_none():
            raise ValidationError('この名前はすでに使われています')