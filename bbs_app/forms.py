from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectMultipleField, widgets, RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,ValidationError
from bbs_app.models import Users
import re

class LoginForm(FlaskForm):
    name = StringField('ユーザーネーム')
    password = PasswordField('パスワード')
    # submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    name = StringField('ユーザーネーム')
    password = PasswordField('パスワード (半角英数字4文字以上)')
    password_confirm = PasswordField('パスワード (確認)')
    # submit = SubmitField('Sign up')

    def validate_name(self, name):
        if len(name.data)>16:
            raise ValidationError('ユーザーネームは16文字以内である必要があります')
        if len(name.data)==0:
            raise ValidationError('ユーザーネームを入力してください')
        if Users.query.filter_by(name=name.data).one_or_none():
            raise ValidationError('この名前はすでに使われています')
        
    def validate_password(self, password):
        pw_pat = re.compile("^[0-9a-zA-Z]+$")
        set_pass=set(password.data)
        set_num=set([str(n) for n in range(10)])

        if len(password.data)<4 or len(password.data) > 25:
            raise ValidationError('パスワードは4文字以上25文字以下')
        
        if not set_pass.intersection(set_num):
            raise ValidationError('パスワードは数字を含む必要があります')
        
        if not pw_pat.match(password.data):
            raise ValidationError('使用できない文字が含まれています')
        
    def validate_password_confirm(self, password_confirm):
        if password_confirm.data!=self.password.data:
            raise ValidationError('パスワードが異なっています')
        
class MessageForm(FlaskForm):
    message = TextAreaField('メッセージ')
    image = FileField('画像', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    def validate_message(self, message):
        if len(message.data)==0:
            print("空文字")
            raise ValidationError('')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class NewThreadForm(FlaskForm):
    def __init__(self,members,*args, **kwargs):
        super(NewThreadForm, self).__init__(*args, **kwargs)
        self.members=members
        self.new_member.choices = [(str(i+1), name) for i, name in enumerate(self.members)]
    thread_name = TextAreaField(label='スレッド名')
    new_member = MultiCheckboxField(label='メンバー')

    def validate_thread_name(self, thread_name):
        if len(thread_name.data)==0:
            print("空文字")
            raise ValidationError('')

class AddMmemberForm(FlaskForm):
    def __init__(self,members,*args, **kwargs):
        super(AddMmemberForm, self).__init__(*args, **kwargs)
        self.members=members
        self.member.choices = [(str(i+1), name) for i, name in enumerate(self.members)]
    member = MultiCheckboxField(label='メンバー')

class DeleteForm(FlaskForm):
    choices = [
        ('no', 'いいえ'),
        ('yes', 'はい、削除します')
    ]
    radio_field = RadioField('Select an option', choices=choices, default='no')

