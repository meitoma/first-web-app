from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,ValidationError
from models import Users

class LoginForm(FlaskForm):
    name = StringField('ユーザーネーム')
    password = PasswordField('パスワード')
    # submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    name = StringField('ユーザーネーム')
    password = PasswordField('パスワード (半角英数字4文字以上)')
    # submit = SubmitField('Sign up')

    def validate_name(self, name):
        if len(name.data)>16:
            raise ValidationError('ユーザーネームは16文字以内である必要があります')
        if Users.query.filter_by(name=name.data).one_or_none():
            raise ValidationError('この名前はすでに使われています')
        
    def validate_password(self, password):
        if len(password.data)<4:
            raise ValidationError('パスワードは4文字以上である必要があります')
        set_pass=set(password.data)
        set_num=set([str(n) for n in range(10)])
        if not set_pass.intersection(set_num):
            raise ValidationError('パスワードは数字を含む必要があります')


class PostForm(FlaskForm):
    message = StringField('メッセージ')
