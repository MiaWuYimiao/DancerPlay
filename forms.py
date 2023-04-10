from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, URL


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(max=30)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    head_img = StringField("Profile image", validators=[URL()])
    fav_type = StringField("Favorite type", validators=[])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

