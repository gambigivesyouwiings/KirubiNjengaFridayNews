from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from sqlalchemy.exc import IntegrityError, ProgrammingError
from functools import wraps
from flask import abort
import bleach
from flask_gravatar import Gravatar
from flask_migrate import Migrate
from PIL import Image, UnidentifiedImageError
from tkinter import messagebox
import requests
import json
import smtplib
import os
from dotenv import load_dotenv
import shutil
from itsdangerous import URLSafeTimedSerializer

# Loading environment variables from a secure .env file
load_dotenv("C:/Users/User/PycharmProjects/environment variables/.env")
map_api = os.getenv("map_api")


# dbFlask was created as a PythonAnywhere MySQL database
user, password = 'fridaynews', 'vmgambii'
host = 'fridaynews.mysql.pythonanywhere-services.com'
db_name = 'fridaynews$default' 

# Initializing the app variables and import classes
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['GOOGLEMAPS_KEY'] = os.getenv("google_key")
Bootstrap(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{password}@{host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECURITY_PASSWORD_SALT"] = os.getenv("SALT")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = os.getenv("USERN")
app.config['MAIL_PASSWORD'] = os.getenv("GMAIL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app=app, db=db)
mail = Mail(app)


video_file_types = ['.WEBM' '.MPG', '.MP2', '.MPEG', '.OGG',
                    '.MPE', '.MPV', '.MP4', '.M4P',
                    '.M4V', '.AVI', '.WMV', '.MOV',
                    '.QT', '.FLV', '.SWF', '.AVCHD']

image_file_types = ['.webp', '.svg', '.png', '.avif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.gif', '.apng']

admin_list = ["gambikimathi@students.uonbi.ac.ke","chadkirubi@gmail.com","njengashwn@gmail.com"]

# This function sends mail to end-users with the Flask-Mail module
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)

# This function generates a unique token that is used for user account authentication
def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])

# This function checks the token and returns the associated email address.
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False

# This saves a post metadata to the database 
def save_post(img_url, video_url=None, title='untitled', author=current_user):
    x = datetime.now()
    full_date = x.strftime("%d %B %Y")
    form_body_content = request.form.get("body")
    new_post = MediaFiles(title=title,
                          video_url=video_url,
                          author=author,
                          img_url=img_url,
                          date=full_date
                          )

    db.session.add(new_post)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Function wrapper to protect some routes from non-admin access
def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.email not in admin_list:
            abort(403)
        return f(*args, **kwargs)

    return wrapper


# CONFIGURE TABLE
class MediaFiles(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    video_url = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=True)
    # This is the parent class ID
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("Users", back_populates="posts")
    comments = relationship("Comments", back_populates="parent_post", cascade="all, delete")


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    posts = relationship("MediaFiles", back_populates="author")
    comments = relationship("Comments", cascade="all, delete", back_populates="comment_author")


class Comments(UserMixin, db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), unique=False, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    comment_author = relationship("Users", back_populates="comments")
    parent_post = relationship("MediaFiles", back_populates="comments", passive_deletes=True)


# with app.app_context():
#     db.create_all()


def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    name = input("Enter email address: ")
    password = input("Enter password: ")
    confirm_password = input("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
    else:
        try:
            user = Users()
            db.session.add(user)
            db.session.commit()
            print(f"Admin with email {email} created successfully!")
        except Exception:
            print("Couldn't create admin user.")

# Home route for landing page
@app.route("/")
def home():
    try:
        posts = db.session.query(MediaFiles).all()
    except ProgrammingError:
        posts = []
        with app.app_context():
            db.create_all()

    return render_template("index.html", admin_list=admin_list, all_posts=posts)


# Register route gets user data from form and saves to database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        user = Users()
        user.name = request.form.get("name")
        user.email = request.form.get("email").lower()
        user.created_on = datetime.now()
        password = request.form.get("password")
        confirmed_pass = request.form.get("confirm")
        if password != confirmed_pass:
            flash("passwords do not much")
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, salt_length=5)
        user.password = hashed_password
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash('User already exists! Try logging in instead')
            return redirect(url_for('login'))
        token = generate_token(user.email)
        confirm_url = url_for("confirm_email", token=token, _external=True)
        html = render_template("email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        flash("successfully registered")
        login_user(user)
        return redirect(url_for("auth"))
    return render_template("register.html", form=form)


# Route to give email auth page
@app.route('/auth2')
def auth():
    return render_template("email-auth.html")


# Login to the website account for user
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        try:
            user = db.session.query(Users).filter_by(email=user_email).first()
            pwhash = user.password
            check = check_password_hash(pwhash, user_password)

        except AttributeError:
            flash("That email seems to not be in our database")
            return redirect(url_for('login'))

        else:
            if check:
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("That password is not correct")
                return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route("/resend")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("home"))
    token = generate_token(current_user.email)
    confirm_url = url_for("confirm_email", token=token, _external=True)
    html = render_template("email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("home"))


# Log out user from their session
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Confirm the user's email
@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    user = Users.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
       flash("Account already confirmed.", "success")
       return redirect(url_for("home"))

    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("home"))


# Contact page route
@app.route("/contact_us", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        # if email != "":
        #     flash("Your message has been sent. Thank you!")
        print(email)
    return render_template("contact.html")


# Gives admin a chance to verify that indeed they want to delete a post
@app.route("/pre_delete/<int:index>", methods=["GET", "POST"])
@admin_only
def pre_delete(index):
    return render_template("delete.html", id=index)


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
@admin_only
def delete(post_id):
    blog_to_delete = db.session.query(MediaFiles).filter_by(id=post_id).first()
    if blog_to_delete.img_url is not None:
        try:
            os.remove(blog_to_delete.img_url)
        except FileNotFoundError:
            pass
    if blog_to_delete.video_url is not None:
        try:
            os.remove(blog_to_delete.video_url)
        except FileNotFoundError:
            pass

    db.session.delete(blog_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

# Route for services page
@app.route("/mservices")
def service():
    return render_template("services.html")


@app.route("/reception")
def gallery():
    return render_template("gallery2.html")


# Route for about page section
@app.route("/about_us")
def about():
    return render_template("about2.html")


@app.route("/msample")
def sample():
    return render_template("sample-inner-page.html")


# Route for uploading posts
@app.route("/upload", methods=["GET", "POST"])
@login_required
@admin_only
def upload():
    if request.method == 'POST':

        # Get the list of files from webpage
        files = request.files.getlist("file")
        is_video = False
        counter = 0
        image_file = None
        video_file = None
        title = "untitled"

        # Iterate for each file and check if it's a video file
        for file in files:

            if os.path.splitext(file.filename)[-1].upper() in video_file_types:
                is_video = True
                counter += 1

        # This control-flow handles video file types and their thumbnails
        if is_video:

            if len(files) != 2:
                flash("video file type needs to be only one pair of a video and its thumbnail")
                return redirect(url_for('upload'))
            elif counter > 1:
                flash("video file type needs to be only one pair of a video and its thumbnail image")
                return redirect(url_for('upload'))

            newpath = f'static/assets/videos/'
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            for file in files:
                file.save(file.filename)
                if os.path.splitext(file.filename)[-1].upper() in video_file_types:
                    video_file = file.filename
                    title = file.filename
                elif os.path.splitext(file.filename)[-1].lower() in image_file_types:
                    image_file = file.filename
                    image = Image.open(image_file)
                    img_resize = image.resize((417, 597))
                    img_resize.save(image_file)
                else:
                    flash("The uploaded file format is not recognized as a video or image filetype")
                    os.remove(file.filename)
                    try:
                        os.remove(video_file)
                    except FileNotFoundError:
                        pass
                    except TypeError:
                        pass
                    return redirect(url_for('upload'))

            for file in files:
                try:
                    shutil.move(file.filename, newpath)
                except shutil.Error:
                    flash("That filename is already in the database. Try renaming and try again")
                    os.remove(video_file)
                    os.remove(image_file)
                    return redirect(url_for('upload'))

            video_file = newpath + video_file
            image_file = newpath + image_file
            save_post(img_url=image_file, video_url=video_file, title=title)
            flash("Files Uploaded Successfully!")
            return redirect(url_for('upload'))

        # This is purely for image type posts

        destination = f"static/assets/img/new_folder/"
        if not os.path.exists(destination):
            os.makedirs(destination)

        for file in files:
            file.save(file.filename)
            if os.path.splitext(file.filename)[-1].lower() not in image_file_types:
                os.remove(file.filename)
            else:
                image = Image.open(file.filename)
                img_resize = image.resize((417, 597))
                img_resize.save(file.filename)

                try:
                    shutil.move(file.filename, destination)
                except shutil.Error:
                    os.remove(file.filename)
                else:
                    image_file = destination + file.filename
                    save_post(img_url=image_file, title=file.filename)
        flash("Files Uploaded Successfully!")
        return redirect(url_for('upload'))
    return render_template("upload.html")


# This route is for editing a blog post thumbnail, title etc.
@app.route("/edit-post/<index>", methods=["GET", "POST"])
@login_required
@admin_only
def edit(index):
    edit_form = CreatePostForm()
    blog_to_edit = db.session.query(MediaFiles).filter_by(id=index).first()

    if edit_form.validate_on_submit():
        img_to_remove = request.args.get("img_to_remove")
        file = edit_form.file.data

        # This filters any non-image file types
        try:
            file.save(file.filename)
            image = Image.open(file.filename)
            img_resize = image.resize((417, 597))
            img_resize.save(file.filename)

        except UnidentifiedImageError:
            os.remove(file.filename)
            flash("That's not an image file!")
            return redirect(url_for('edit', index=index))

        # This moves the uploaded file to the videos folder from the project root

        destination = f"static/assets/videos/"
        try:
            shutil.move(file.filename, destination)
        except shutil.Error:
            os.remove(file.filename)
            flash("That file already exists")
            return redirect(url_for('edit', index=index))
        else:
            image_file = destination + file.filename

        # This removes the original image after successfully moving the new file
        try:
            if img_to_remove != file.filename:
                os.remove(img_to_remove)
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        flash("Files Uploaded Successfully!")

        # now to effect these changes in the database
        try:
            if edit_form.title.data != "":
                blog_to_edit.title = edit_form.title.data
        except IntegrityError:
            flash("Two blog posts can't have the same title")
            return redirect(url_for('edit', index=index))
        finally:
            blog_to_edit.img_url = image_file
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
