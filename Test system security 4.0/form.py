from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from email_validator import validate_email, EmailNotValidError

class RegisterForm(FlaskForm):
    username = StringField('username',[DataRequired(message="Please enter between 4 and 15 characters"), Length(min=4, max=15)])
    password = PasswordField('password',[DataRequired(message="Please enter between 8 and 15 characters"), Length(min=8, max=15)])
    email = StringField('email', [DataRequired(message="")])
    mobile = StringField('mobile', [DataRequired(), Length(min=8, max=8)])
    recaptcha = RecaptchaField()
    submit = SubmitField("submit")

    def validate_mobile(form, field):
        if len(field.data) > 8 or not field.data.isdigit():
            raise ValidationError('Invalid phone number.')

    def validate_email(form, field):
        try:
            validate_email(field.data)
        except EmailNotValidError:
            raise ValidationError('Invalid Email.')



class LoginForm(FlaskForm):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("submit")
