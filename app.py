from flask import Flask, redirect, render_template, session, flash, url_for, request, g
from flask_debugtoolbar import DebugToolbarExtension
from models import User, connect_db, db, FavPlaylist, Playlist, Music, PlaylistMusic
from forms import UserForm, LoginForm
from search import search_videos
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"
CURR_PLAYLIST_KEY = "curr_playlist"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///dancerplay_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "12345"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

########### User Register, Login, Logout ##############


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User.register(
            username = form.username.data, 
            password = form.password.data, 
            email = form.email.data, 
            first_name = form.first_name.data, 
            last_name = form.last_name.data,
            head_img = form.head_img.data or User.head_img.default.arg,
            fav_type = form.fav_type.data or User.fav_type.default.arg,
            )

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('user_create_form.html', form=form)

        do_login(new_user)

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
            do_login(user)
            return redirect(url_for('user_detail_page', username = user.username))
        else:
            form.username.errors = ['Invalid username/password.']
    
    return render_template("user_login_form.html", form=form)


@app.route('/logout')
def logout_user():
    """Handle logout of user."""
    do_logout()

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



#################  Search and add music playlist #############
@app.before_request
def add_playlist_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_PLAYLIST_KEY in session:
        g.playlist = Playlist.query.get(session[CURR_PLAYLIST_KEY])

    else:
        g.playlist = None


# Search routes
@app.route('/search')
def search_music():

    style = request.args.get("style")
    type = request.args.get("type")
    length = request.args.get("length")

    playlist, durationTotal, img_url = search_videos(style, type, length)

    # Add searched list to DB
    new_playlist = Playlist(name='new playlist',
                            description=f"A list of {style} {type}",
                            image_url=img_url,
                            type=type,
                            length=durationTotal)
    db.session.add(new_playlist)
    db.session.commit()

    # add new playlist to session
    session[CURR_PLAYLIST_KEY] = new_playlist.id
    # Add new playlist to Flask global
    # g.playlist = new_playlist

    min = int(durationTotal/60)
    sec = int(durationTotal%60)
    totalTime = ''.join(map(str,[min, ' min ', sec, ' sec']))

    return render_template('index.html', playlist=playlist, totalTime=totalTime, style=style, type=type, length=length)


@app.route('/users/like', methods=["GET","POST"])
def playlist_add():
    """Add a playlist"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    playlist = g.playlist
    if playlist:

        playlist.name = f"playlist-{playlist.id}"
        g.user.playlists.append(playlist)
        db.session.commit()

    return redirect('/')


@app.route('/users/<username>/mylist', methods=["GET"])
def show_user_playlist(username):
    """show user's playlists page"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(username)

    return render_template('user_playlist.html', user=user)

################ Homepage and error pages ################

@app.route('/')
def home_page():
    style = 'Ballet'
    type = 'Barre'
    length = 20
    playlist = []
    return render_template('index.html', playlist=playlist, style=style, type=type, length=length)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404