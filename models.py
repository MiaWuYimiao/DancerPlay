"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    head_img = db.Column(db.Text)
    fav_type = db.Column(db.String(30))

    playlists = db.relationship(
        "Playlist", 
        secondary="favoriteplaylists")


    @classmethod
    def register(cls, username, password, first_name, last_name, email, head_img, fav_type):
        """Register user w/hased password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd and other info
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email, head_img=head_img, fav_type=fav_type)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class FavPlaylist(db.Model):
    __tablename__ = "favoriteplaylists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), db.ForeignKey('users.username'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))


class Playlist(db.Model):
    """Playlist."""
    __tablename__ = 'playlists'

    # ADD THE NECESSARY CODE HERE
    id = db.Column( db.Integer, primary_key=True, autoincrement=True,)
    name = db.Column( db.VARCHAR(50), nullable=False,)
    description = db.Column( db.Text, nullable=False,)
    image_url = db.Column( db.Text, nullable=False,)
    type = db.Column( db.String(30), nullable=False,)
    length = db.Column( db.Integer, nullable=False,)

    musics = db.relationship('Music', secondary='playlistmusic', backref='playlists')


class Music(db.Model):
    """Music."""
    __tablename__ = 'musics'

    # ADD THE NECESSARY CODE HERE
    id = db.Column( db.Integer, primary_key=True, autoincrement=True,)
    title = db.Column( db.String(50), nullable=False,)
    genre = db.Column( db.String(30), nullable=False,)
    type = db.Column( db.String(30), nullable=False,)
    length = db.Column( db.Integer, nullable=False,)
    videoId = db.Column( db.Text, nullable=False,)
    image_url = db.Column( db.Text, nullable=False,)


class PlaylistMusic(db.Model):
    """Mapping of a playlist to a music."""
    __tablename__ = 'playlistmusic'

    # ADD THE NECESSARY CODE HERE
    id = db.Column( db.Integer, primary_key=True, autoincrement=True,)
    playlist_id = db.Column( db.Integer, db.ForeignKey('playlists.id'))
    music_id = db.Column( db.Integer, db.ForeignKey('musics.id'))


