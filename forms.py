from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired
from flask_ckeditor import CKEditorField


# WTForm for posts
class CreatePostForm(FlaskForm):
    title = StringField("New Post Title")
    file = FileField("New Post Image", id="fike", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name = StringField("Enter your name", validators=[DataRequired()])
    email = EmailField("Enter your email address", validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField("Repeat password", validators=[InputRequired(), DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Sign me Up")


class LoginForm(FlaskForm):
    email = EmailField("Enter your email address", validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Sign me In")


class CommentForm(FlaskForm):
    body = CKEditorField("Blog Comment", validators=[DataRequired()])
    submit = SubmitField("Add comment")
