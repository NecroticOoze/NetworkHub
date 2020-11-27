from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[])
    password = PasswordField('Password',validators=[])
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[])
    password = PasswordField('Password',validators=[])
    confirm_password = PasswordField('Confirm Password',validators=[])

    submit = SubmitField('Submit')

class UploadFileForm(FlaskForm):
    path = StringField('Path', validators=[])
    drive = SelectField('Drive',choices=[('-1','Select ...')], validators=[])
    uploaded_file = FileField('Upload File', validators=[])

    submit = SubmitField('Upload')
    