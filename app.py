from flask import Flask, redirect, render_template, session, flash, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db, FavPlaylist, Playlist, Music, PlaylistMusic
from forms import UserForm, LoginForm
from search import search_videos
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///dancerplay_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "12345"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    style = 'Latin'
    type = 'Barre'
    length = 20
    return render_template('index.html', style=style, type=type, length=length)


########### User Register, Login, Logout ##############

@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('user_create_form.html', form=form)
        session['username'] = new_user.username
        flash(f"{new_user.username} added.")
        return redirect(url_for('user_detail_page', username=new_user.username))
    
    else:
        return render_template("user_create_form.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(url_for('user_detail_page', username = user.username))
        else:
            form.username.errors = ['Invalid username/password.']
    
    return render_template("user_login_form.html", form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>')
def user_detail_page(username):
    if "username" not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login_page'))

    user = User.query.get_or_404(username)
    return render_template("user_detail.html", user=user)

@app.route('/users/<username>/delete')
def delete_user(username):
    if "username" not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login_page'))

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')



#################  Search for videos #############

# Search routes
@app.route('/search')
def search_music():

    style = request.args.get("style")
    type = request.args.get("type")
    length = request.args.get("length")

    playlist, durationTotal = search_videos(style, type, length)

    min = int(durationTotal/60)
    sec = int(durationTotal%60)
    totalTime = ''.join(map(str,[min, ' min ', sec, ' sec']))

    return render_template('index.html', playlist=playlist, totalTime=totalTime, style=style, type=type, length=length)


