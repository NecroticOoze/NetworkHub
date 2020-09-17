from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField

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
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a \
            different one.')

class UploadFileForm(FlaskForm):
    path = StringField('Path', validators=[])
    drive = SelectField('Drive',choices=[('-1','Select ...')], validators=[])
    uploaded_file = FileField('Upload File', validators=[])

    submit = SubmitField('Upload')
    